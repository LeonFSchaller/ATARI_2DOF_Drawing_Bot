import numpy as np
from scipy.ndimage import gaussian_filter1d
from math import sqrt, pow, atan2, sin, cos, pi, exp
from scipy.ndimage import gaussian_filter1d

DECAY_FACTOR = 1.8
DAMPING_FACTOR = 0.95

class Simulator:

    def __call__(self, points, damping_factor=DAMPING_FACTOR, decay_factor=DECAY_FACTOR):
        _points = self._apply_error_rule(points, damping_factor, decay_factor)

        return _points
    
    def _get_phase(self, point, prev_point):
        _pointing_vector = [point[0]-prev_point[0], point[1]-prev_point[1]]
        _phase = atan2(_pointing_vector[1], _pointing_vector[0])
        return _phase
    
    def _get_point_from_phase(self, phase, radius):
        _scaler = radius
        _x_offset = _scaler * cos(phase)
        _y_offset = _scaler * sin(phase)
        return [_x_offset, _y_offset]

    def _apply_error_rule(self, points, damping_factor, decay_factor):
        _new_points = [[0, 0], points[0]]
        _prev_phase_offset = 0

        for _index in range(1, len(points)):
            # add offset to current point
            _point = points[_index]
            _radius = sqrt(pow(_point[0]-_new_points[-1][0], 2) + pow(_point[1] - _new_points[-1][1], 2))
            #print(f'Current point: {_point};    Previous point: {_new_points[-1]}')
            #print(f'Radius: {_radius}')

            # Calculate phase of vector between current point and last point; Same for previous point and the one before
            _phase = self._get_phase(_point, _new_points[-1])
            _prev_phase = self._get_phase(_new_points[-1], _new_points[-2])
            #print(f'current phase: {_phase};    Prev phase: {_prev_phase}')

            # Calculate difference between the last two phases
            _phase_difference = _phase-_prev_phase
            #print(f'Phase difference before: {_phase_difference}')
            if abs(_phase_difference) > pi:
                _phase_difference = -np.sign(_phase_difference) * ((2 * pi) - abs(_phase_difference))
            #print(f'Phase difference after: {_phase_difference}')

            damping = -(1/(1 + exp(damping_factor * abs(_prev_phase_offset))))
            _phase_offset = damping * (_phase_difference) * decay_factor
            #_phase_offset = -0.65 * (_phase_difference)
            #print(f'Phase offset: {_phase_offset}')

            # Calculate offset for next point
            _new_vector = self._get_point_from_phase(_phase+_phase_offset, _radius)
            #print(f'Offset vector: {_new_vector}')

            _new_point = [_new_points[-1][0]+_new_vector[0], _new_points[-1][1]+_new_vector[1]]
            #print(f'New point: {_new_point}')

            # overwritting all 'prev'-parameters with current parameters
            _new_points.append(_new_point)
            _prev_phase_offset = _phase_offset
            #print(f'----------------------------------')
        
        _new_points.pop(0)
        return _new_points

class ExponentialDecaySimulator:
    def __call__(self, points, gain, **kwargs):
        _points = self.apply_error_rule(points, gain, **kwargs)
        return _points
        
    def _get_phase(self, point, prev_point):
        _pointing_vector = [point[0]-prev_point[0], point[1]-prev_point[1]]
        _phase = atan2(_pointing_vector[1], _pointing_vector[0])
        return _phase
    
    def _get_point_from_phase(self, phase, radius):
        _scaler = radius
        _x_offset = _scaler * cos(phase)
        _y_offset = _scaler * sin(phase)
        return [_x_offset, _y_offset]
    
    def _phase_offsets_to_points(self, phase_offsets, normals, points):
        _points_x = points[:, :1] + normals[:, :1] * phase_offsets
        _points_y = points[:, 1:] + normals[:, 1:] * phase_offsets
        return np.hstack([_points_x, _points_y])
    
    def _get_phase_difference(self, phases):
        _phase_differences = []

        for _index in range(1, len(phases)):
            
            _phase = phases[_index]
            _prev_phase = phases[_index - 1]
            _phase_difference = _phase-_prev_phase

            if abs(_phase_difference) > pi:
                _phase_difference = -np.sign(_phase_difference) * ((2 * pi) - abs(_phase_difference))
            
            _phase_differences.append(_phase_difference)
        
        return np.array(_phase_differences)
    
    def _points_to_phases(self, trajectory):
        _points = np.array(trajectory)[1:]
        _prev_points = np.array(trajectory)[:-1]
        _direction_vectors = _points - _prev_points
        _direction_vectors = _direction_vectors.T
        _phases = np.arctan2(_direction_vectors[1], _direction_vectors[0])
        return _phases
    
    def apply_error_rule(self, points, gain=5, damping=0.25, freq=1, non_linearity=1, length=60):
        _points = np.array(points)

        _phases = self._points_to_phases(points)

        _normals_to_phases = np.array([np.cos(_phases + np.pi/2), np.sin(_phases + np.pi/2)]).T
        _normals_to_phases = np.append(_normals_to_phases, np.zeros((1, 2)), axis=0)

        _phase_differences = self._get_phase_difference(_phases)
        _normalized_phase_differences = _phase_differences / np.pi
        _weighted_normalized_phase_differences = 0.5 + np.tanh(_normalized_phase_differences * non_linearity) / 2

        oscillation = (1 / np.exp((damping) * np.arange(length))) * np.sin(freq * np.arange(length))
        oscillation = (oscillation / np.max(oscillation) + 1e-8) * -gain

        _point_offsets = np.zeros(np.shape(_phases))
        for _index in range(len(_point_offsets)-length):
            _point_offsets[_index:_index+length] = _point_offsets[_index:_index+length] + (oscillation * _weighted_normalized_phase_differences[_index])

        _point_offsets = np.append(0, _point_offsets)
        _point_offsets = _point_offsets.reshape(-1, 1)

        _new_points = self._phase_offsets_to_points(_point_offsets, _normals_to_phases, _points)
        
        return _new_points



if __name__ == '__main__':
    error_simulator = Simulator(strength=100, pattern_length=10)
    #print(error_simulator.pattern_x)
    #points = [[1,1], [1,1], [1,1], [1,1], [1,1], [1,1], [1,1], [1,1], [1,1]]
    points = [[0.0,0.0], [1.0, 2.0], [2.0,3.0], [3.0,4.0], [4.0, 3.0], [5.0,6.0], [6.0, 9.0], [7.0,8.0], [8.0,9.0], [9.0, 0]]
    print(error_simulator(points))