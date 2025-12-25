import pygame

class Widget:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

class Button(Widget):
    def __init__(self, x, y, width, height, text, callback, color=(50, 50, 50), text_color=(255, 255, 255)):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255))
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
        self.hovered = False

    def draw(self, screen):
        if not self.visible: return
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.visible: return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                if self.callback:
                    self.callback()

class Window(Widget):
    def __init__(self, x, y, width, height, title):
        super().__init__(x, y, width, height)
        self.title = title
        self.children = []
        self.dragging = False
        self.drag_offset = (0, 0)
        self.font = pygame.font.Font(None, 28)

    def add_child(self, widget):
        # Adjust widget pos relative to window?
        # For simplicity, absolute pos for now, or we implement relative layout
        widget.rect.x += self.rect.x
        widget.rect.y += self.rect.y
        self.children.append(widget)

    def draw(self, screen):
        if not self.visible: return
        # Draw Frame
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        # Title Bar
        pygame.draw.rect(screen, (60, 60, 80), (self.rect.x, self.rect.y, self.rect.width, 30))
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (self.rect.x + 10, self.rect.y + 5))

        for child in self.children:
            child.draw(screen)

    def handle_event(self, event):
        if not self.visible: return

        # Window Dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                title_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 30)
                if title_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_offset = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_offset[0] - self.rect.x
                dy = event.pos[1] - self.drag_offset[1] - self.rect.y
                self.rect.x += dx
                self.rect.y += dy
                # Update children
                for child in self.children:
                    child.rect.x += dx
                    child.rect.y += dy

        for child in self.children:
            child.handle_event(event)
