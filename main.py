import pygame
import ctypes
from tensorflow.keras.models import load_model
import numpy as np


class GUI(object):
    def __init__(self):
        # This was created for 1080p screen but should run properly in other resolutions
        ctypes.windll.user32.SetProcessDPIAware()
        true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        self.screen_width = true_res[0]
        self.screen_height = true_res[1]
        self.scale_x = self.screen_width / 1980
        self.scale_y = self.screen_height / 1080
        self.window = pygame.display.set_mode(true_res, pygame.FULLSCREEN)

        # Font used
        self.font = pygame.font.SysFont('agencyfb', 100, True, False)

        # Frames per second of the application (cannot be made too low otherwise clicks will not work)
        # fps = 0 gives maximum speed but at that speed animations will not be visible
        self.fps = 200

        # Loading images
        pic = pygame.image.load('assets/home.jpg').convert()
        self.home = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/building1.jpg').convert()
        self.building1 = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))
        pic = pygame.image.load('assets/building2.jpg').convert()
        self.building2 = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/building3.jpg').convert()
        self.building3 = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/reset.jpg').convert()
        self.reset = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/predict.jpg').convert()
        self.predict = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/result.jpg').convert()
        self.result = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        pic = pygame.image.load('assets/reset_result.jpg').convert()
        self.reset_result = pygame.transform.scale(pic, (int(1980 * self.scale_x), int(1080 * self.scale_y)))

        # Loading sound
        self.click_audio = pygame.mixer.Sound('assets/click.wav')
        self.building_audio = pygame.mixer.Sound('assets/building.wav')

        # Following variables are used to determine which image to display
        self.count_reset = self.fps
        self.count_predict = self.fps
        self.count_building = 0
        self.reset_state = False
        self.predict_state = False
        self.predicted = False
        self.building = False

        # Used to store all clicked points on drawing surface
        self.points = []

        # If a pixed is clicked, a circle is drawn with that pixel as the center, having the following radius
        self.radius = int(20 * self.scale_x)

        # Defining drawing surface
        rect = pygame.Rect(642 * self.scale_x, 436 * self.scale_y, 392 * self.scale_x, 392 * self.scale_y)
        self.drawing_surface = self.window.subsurface(rect)

        # Loading model created by CNN.py
        self.model = load_model("model.h5")

        # Predicted value
        self.prediction = 0

    def function(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(self.fps)

            # To check for key presses
            keys = pygame.key.get_pressed()

            # Getting the current position of mouse
            mouse = pygame.mouse.get_pos()

            # To check for mouse clicks
            click = pygame.mouse.get_pressed()

            # To check if quit button (top right x button) is pressed (not needed in fullscreen mode)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Escape button can be used to quit
            if keys[pygame.K_ESCAPE]:
                return

            self.count_reset += 1
            self.count_predict += 1

            # Reset button
            if not self.building and self.count_reset > self.fps / 2:
                if 1136 * self.scale_x < mouse[0] < 1543 * self.scale_x and 512 * self.scale_y < mouse[1] < 579 * self.scale_y:
                    if click[0] == 1:
                        self.click_audio.play()
                        self.count_reset = 0
                        self.reset_state = True

            # Predict button
            if not self.building and not self.predicted and self.count_predict > self.fps / 2:
                if 1136 * self.scale_x < mouse[0] < 1543 * self.scale_x and 662 * self.scale_y < mouse[1] < 729 * self.scale_y:
                    if click[0] == 1:
                        self.click_audio.play()
                        self.count_predict = 0
                        self.prediction = self.pred()
            # Increase counter if building animation is being done
            if self.building:
                self.count_building += 1

            # Drawing
            if not self.building:
                if click[0] == 1:
                    if (642 + self.radius - 1) * self.scale_x < mouse[0] < (642 + 392 - self.radius) * self.scale_x and (436 + self.radius - 1) * self.scale_y < mouse[1] < (436 + 392 - self.radius) * self.scale_y:
                        self.points.append((mouse[0], mouse[1]))

            self.draw()

    def draw(self):
        if self.reset_state:
            # Display reset button animation
            if self.count_reset < self.fps // 4:
                if self.predicted:
                    self.window.blit(self.reset_result, (0, 0))
                else:
                    self.window.blit(self.reset, (0, 0))
            else:
                self.points = []
                self.reset_state = False
                self.predicted = False

        elif self.predict_state:
            # Display predict button animation
            if self.count_predict < self.fps // 4:
                self.window.blit(self.predict, (0, 0))
            else:
                self.predict_state = False
                self.building = True
                self.building_audio.play()

        elif self.building:
            # Display building animation
            if self.count_building < self.fps // 2.2:
                self.window.blit(self.building1, (0, 0))
            elif self.count_building < 2 * self.fps // 2.2:
                self.window.blit(self.building2, (0, 0))
            elif self.count_building < 3 * self.fps // 2.2:
                self.window.blit(self.building3, (0, 0))
            else:
                self.building = False
                self.count_building = 0
                self.predicted = True

        elif self.predicted:
            # Display predicted number
            self.window.blit(self.result, (0, 0))
            text_obj = self.font.render(str(self.prediction), True, (0, 0, 0))
            self.window.blit(text_obj, (1290, 258))

        else:
            # Display default screen
            self.window.blit(self.home, (0, 0))

        for point in self.points:
            # Display digit drawn by user
            pygame.draw.circle(self.window, (0, 0, 0), point, self.radius)

        pygame.display.update()

    def pred(self):
        self.predict_state = True

        # Obtaining the pixels in drawing surface
        pixels = pygame.PixelArray(self.drawing_surface)
        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                # Replacing background color of drawing surface with white
                if pixels[i][j] == 0xdddddd:
                    pixels[i][j] = 0xffffff

        # Converting drawing surface to 28 x 28 array
        ar = []
        for i in range(28):
            temp = []
            for j in range(28):
                count = 0.0
                for x in range(int(14 * self.scale_x)):
                    for y in range(int(14 * self.scale_y)):
                        if pixels[i * int(14 * self.scale_x) + x][j * int(14 * self.scale_x) + y] == 0x000000:
                            count += 1
                temp.append([int(count / (int(14 * self.scale_x) * int(14 * self.scale_x)))])
            ar.append(temp)

        # Array needs to be oriented properly due to different coordinate systems
        ar = np.array(ar)
        ar = np.rot90(ar)
        ar = np.flipud(ar)

        # Using CNN model to predict digit
        # Model gives array of size 10 containing probability of each digit
        pred = self.model.predict(np.array([ar]))
        return pred.argmax()


if __name__ == '__main__':
    # Initializing pygame
    pygame.init()

    # Creating GUI object
    obj = GUI()

    # Setting window title
    pygame.display.set_caption("Handwriting Recognizer")

    # Calling function
    obj.function()

    # Closing pygame object
    pygame.quit()
