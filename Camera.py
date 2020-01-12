class Camera:
    def __init__(self, width, height, x=0, y=0):
        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)