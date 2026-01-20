
class PidModel:
    def __init__(self):
        self.integral = 0
        self.prev_error = 0
        self.current_val = 0
        self.velocity = 0

    def reset(self):
        self.integral = 0
        self.prev_error = 0
        self.current_val = 0
        self.velocity = 0

    def update(self, setpoint, kp, ki, kd, dt=0.1):
        error = setpoint - self.current_val
        
        
        p_term = kp * error
        
        
        self.integral += error * dt
        i_term = ki * self.integral
        
        
        d_term = kd * (error - self.prev_error) / dt
        self.prev_error = error
        

        output = p_term + i_term + d_term
        

        self.velocity += (output - self.velocity) * 0.5 * dt
        self.current_val += self.velocity * dt
        
        return self.current_val
