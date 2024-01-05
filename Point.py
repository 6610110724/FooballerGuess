    def add_point_collector(self):
        # Add a point collector at a random position
        x = randint(self.ball_radius, self.width - self.ball_radius)
        y = randint(self.ball_radius, self.height - self.ball_radius)
        self.points.append((x, y))

        # Draw the point collector on the canvas
        with self.canvas:
            Color(1, 0, 0)  # Red color for point collectors
            Ellipse(pos=(x - self.ball_radius, y - self.ball_radius),
                    size=(self.ball_radius * 2, self.ball_radius * 2))

    def check_collision(self):
        # Check collision with point collectors
        for point in self.points:
            distance = ((self.ball_pos[0] - point[0])**2 + (self.ball_pos[1] - point[1])**2)**0.5
            if distance < self.ball_radius:
                # Ball collided with a point collector
                self.score += 10
                self.remove_point_collector(point)
                self.add_point_collector()

    def remove_point_collector(self, point):
        # Remove point collector from the canvas and the list
        self.points.remove(point)
        self.canvas.clear()  # Clear the canvas
        self.draw_ball()  # Redraw the ball
        for p in self.points:
            with self.canvas:
                Color(1, 0, 0)
                Ellipse(pos=(p[0] - self.ball_radius, p[1] - self.ball_radius),
                        size=(self.ball_radius * 2, self.ball_radius * 2))




    