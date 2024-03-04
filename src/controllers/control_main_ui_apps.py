from PyQt6 import QtCore


class ControlApps:
    def __init__(self, main_ui):
        self.ui = main_ui

    def button_menu(self, maxWidth, enable):
        """Animates the left-side menu of the application.

        Args:
            maxWidth (int): The maximum width the menu should extend to.
            enable (bool): Whether to enable or disable the animation.

        Returns:
            None.
        """
        if enable:
            width = self.ui.frame_button_left.width()
            maxExtend = maxWidth
            standard = 70

            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QtCore.QPropertyAnimation(self.ui.frame_left, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()

    def button_about_us(self, enable, theme):
        """Animate the "About Us" button and expand the right-hand additional frame.

        Args:
            enable (bool): True to enable the animation and expand the frame, False to disable.
            theme (str): The current theme ("light" or "dark").

        Returns:
            None
        """
        if enable:
            # GET WIDTH
            width = self.ui.frame_additional_right.width()
            widthLeftBox = self.ui.frame_additional_left.width()
            standard = 0

            style = self.ui.btn_setting.styleSheet()

            # SET MAX WIDTH
            if widthLeftBox != 0:
                color = "background-color: rgb(238, 238, 236);"
                color_dark = "background-color: rgb(33, 37, 43);"
                self.ui.btn_setting.setStyleSheet(style + color)
                if theme == "dark":
                    self.ui.btn_setting.setStyleSheet(style + color_dark)

            self.start_box_animation(widthLeftBox, width, "right")

    def setting_menu(self, enable, theme):
        """Toggle the visibility of the additional left frame and update the theme of the settings button.

        Args:
            enable: A boolean indicating whether the additional left frame should be shown or not.
            theme: A string specifying the theme of the application. It can be "light" or "dark".

        Returns:
            None.
        """
        if enable:
            width = self.ui.frame_additional_left.width()
            widthRightBox = 0
            standard = 0

            style = self.ui.btn_setting.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                color = "background-color: rgb(255, 255, 255);"
                color_dark = "background-color: rgb(44, 49, 58);"
                self.ui.btn_setting.setStyleSheet(style + color)
                if theme == "dark":
                    self.ui.btn_setting.setStyleSheet(style + color_dark)

            else:
                color = "background-color: rgb(238, 238, 236);"
                color_dark = "background-color: rgb(33, 37, 43);"
                self.ui.btn_setting.setStyleSheet(style + color)
                if theme == "dark":
                    self.ui.btn_setting.setStyleSheet(style + color_dark)

            self.start_box_animation(width, widthRightBox, "left")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        """Animate the left and right boxes to slide in or out.

        Args:
            left_box_width (int): The current width of the left box.
            right_box_width (int): The current width of the right box.
            direction (str): The direction in which to animate the boxes, either "left" or "right".

        Returns:
            None
        """
        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0

        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0

        # ANIMATION LEFT BOX
        left_box = QtCore.QPropertyAnimation(self.ui.frame_additional_left, b"minimumWidth")
        left_box.setDuration(500)
        left_box.setStartValue(left_box_width)
        left_box.setEndValue(left_width)
        left_box.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)

        # # ANIMATION RIGHT BOX
        right_box = QtCore.QPropertyAnimation(self.ui.frame_additional_right, b"minimumWidth")
        right_box.setDuration(500)
        right_box.setStartValue(right_box_width)
        right_box.setEndValue(right_width)
        right_box.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)

        # GROUP ANIMATION
        self.group = QtCore.QParallelAnimationGroup()
        self.group.addAnimation(left_box)
        self.group.addAnimation(right_box)
        self.group.start()




