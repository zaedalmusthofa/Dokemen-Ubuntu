"""
Class to control manipulate image
"""


class ControlResultImage:

    @staticmethod
    def zoom_in(current_size):
        """Increases the current size by 100 and returns the new size.

        Args:
            current_size (int): The current size.

        Returns:
            int: The new size after increasing by 100.
        """
        # If the current size of the image is larger than 6000, no changes made
        if current_size > 6000:
            pass
        # Else, increase the size by 100
        else:
            current_size += 100
        # Return the new size
        return current_size

    @staticmethod
    def zoom_out(current_size):
        """Decreases the `current_size` by 100, unless it's already below 640.

        Args:
            current_size (int): The current size to decrease by 100.

        Returns:
            int: The new size after decreasing by 100, or the original `current_size` if it's already below 640.
        """
        if current_size < 640:
            pass
        else:
            current_size -= 100
        return current_size

    @staticmethod
    def rotate_left(current_angle):
        """Rotates the image to the left by 5 degrees.

        Args:
            current_angle (int): The current angle of rotation in degrees.

        Returns:
            int: The new angle of rotation after rotating left by 5 degrees.

        """
        if current_angle == 180:
            pass
        else:
            current_angle += 5
        return current_angle

    @staticmethod
    def rotate_right(current_angle):
        """
        Rotates the given angle to the right by 5 degrees.

        Args:
            current_angle (int): The current angle in degrees to be rotated.

        Returns:
            int: The new angle after rotation to the right.
        """
        if current_angle == -180:
            pass
        else:
            current_angle -= 5
        return current_angle

