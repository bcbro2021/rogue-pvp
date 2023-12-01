class Anim_manager():
    def __init__(self,default_anim="idle"):
        self.animations = {}
        self.frame = 0
        self.current_anim = default_anim
        self.animation_delays = {}
    
    def add_animation(self, name,frames,delay=10):
        self.animations[name] = frames
        self.animation_delays[name] = [delay,delay]

    def play_animation(self, name):
        self.animation_delays[name][0] -= 1
        self.current_anim = name
        if self.animation_delays[name][0] <= 0:
            if self.frame < len(self.animations[name])-1:
                self.frame += 1
            elif self.frame >= len(self.animations[name])-1:
                self.frame = 0
            
            self.animation_delays[name][0] = self.animation_delays[name][1]
    
    def get_current_anim_frame(self):
        return self.animations[self.current_anim][self.frame]