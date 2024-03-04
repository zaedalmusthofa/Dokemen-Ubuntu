import os
from PyQt6 import QtCore, QtGui


class GetResourcesIcon:
    def __init__(self):
        self.__realpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        QtCore.QDir.addSearchPath("icons", CURRENT_DIRECTORY + "/icons")

    def get_icon_moilapp(self):
        return QtGui.QIcon(self.__realpath + "/icons/moil_icon.png")

    def get_icon_user(self):
        return QtGui.QIcon(self.__realpath + "/icons/user.svg")

    # icon feature
    def get_icon_fisheye_24px(self):
        return QtGui.QIcon(self.__realpath + "/icons/fisheye.png")

    def get_icon_fisheye_200px(self):
        return QtGui.QIcon(self.__realpath + "/icons/fisheye_ori.png")

    def get_icon_anypoint_24px(self):
        return QtGui.QIcon(self.__realpath + "/icons/any_point.png")

    def get_icon_anypoint_old_icon(self):
        return QtGui.QIcon(self.__realpath + "/icons/anypoint.png")

    def get_icon_anypoint_128px(self):
        return QtGui.QIcon(self.__realpath + "/icons/any_point_ori.png")

    def get_icon_panorama_24px(self):
        return QtGui.QIcon(self.__realpath + "/icons/panorama_.png")

    def get_icon_panorama_old_icon(self):
        return QtGui.QIcon(self.__realpath + "/icons/panorama.png")

    def get_icon_panorama_128px(self):
        return QtGui.QIcon(self.__realpath + "/icons/panorama_or.png")

    # arrow
    def get_icon_arrow_down(self):
        return QtGui.QIcon(self.__realpath + "/icons/arrow_down.svg")

    def get_icon_arrow_left(self):
        return QtGui.QIcon(self.__realpath + "/icons/arrow_left.svg")

    def get_icon_arrow_right(self):
        return QtGui.QIcon(self.__realpath + "/icons/arrow_right.svg")

    def get_icon_arrow_up(self):
        return QtGui.QIcon(self.__realpath + "/icons/arrow_up.svg")

    def get_icon_up(self):
        return QtGui.QIcon(self.__realpath + "/icons/up.png")

    def get_icon_down(self):
        return QtGui.QIcon(self.__realpath + "/icons/down.png")

    def get_icon_left(self):
        return QtGui.QIcon(self.__realpath + "/icons/left.png")

    def get_icon_right(self):
        return QtGui.QIcon(self.__realpath + "/icons/right.png")

    def get_icon_center(self):
        return QtGui.QIcon(self.__realpath + "/icons/center.png")

    # media player icon
    def get_icon_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/video.svg")

    def get_icon_square(self):
        return QtGui.QIcon(self.__realpath + "/icons/square.svg")

    def get_icon_play_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/play.svg")

    def get_icon_pause_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/pause.svg")

    def get_icon_resume_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/resume.png")

    def get_icon_rewind_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/rewind.svg")

    def get_icon_forward_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/forward.svg")

    def get_icon_skip_rewind_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/skip-back.svg")

    def get_icon_skip_forward_video(self):
        return QtGui.QIcon(self.__realpath + "/icons/skip-forward.svg")

    # zoom in zoom out icon
    def get_icon_zoom_in(self):
        return QtGui.QIcon(self.__realpath + "/icons/zoom-in.svg")

    def get_icon_zoom_out(self):
        return QtGui.QIcon(self.__realpath + "/icons/zoom-out.svg")

    # rotate
    def get_icon_rotate_ccw(self):
        return QtGui.QIcon(self.__realpath + "/icons/rotate-ccw.svg")

    def get_icon_rotate_cw(self):
        return QtGui.QIcon(self.__realpath + "/icons/rotate-cw.svg")

    # show hide
    def get_icon_show(self):
        return QtGui.QIcon(self.__realpath + "/icons/show_.png")

    def get_icon_mouse_pointer(self):
        return QtGui.QIcon(self.__realpath + "/icons/mouse-pointer.png")

    def get_icon_hide(self):
        return QtGui.QIcon(self.__realpath + "/icons/hide_.png")

    # shape
    def get_icon_sun(self):
        return QtGui.QIcon(self.__realpath + "/icons/sun.svg")

    def get_icon_moon(self):
        return QtGui.QIcon(self.__realpath + "/icons/moon.svg")

    def get_icon_plus(self):
        return QtGui.QIcon(self.__realpath + "/icons/plus.svg")

    def get_icon_cross_x(self):
        return QtGui.QIcon(self.__realpath + "/icons/x.svg")

    def get_icon_setting(self):
        return QtGui.QIcon(self.__realpath + "/icons/settings.svg")

    def get_icon_opened_folder(self):
        return QtGui.QIcon(self.__realpath + "/icons/opened-folder.png")

    def get_icon_trash(self):
        return QtGui.QIcon(self.__realpath + "/icons/trash.svg")

    def get_icon_text(self):
        return QtGui.QIcon(self.__realpath + "/icons/text.svg")

    def get_icon_help(self):
        return QtGui.QIcon(self.__realpath + "/icons/help-circle.svg")

    def get_icon_info(self):
        return QtGui.QIcon(self.__realpath + "/icons/info.svg")

    def get_icon_minus(self):
        return QtGui.QIcon(self.__realpath + "/icons/minus-circle.svg")

    def get_icon_link(self):
        return QtGui.QIcon(self.__realpath + "/icons/link.svg")

    def get_icon_maximize_view(self):
        return QtGui.QIcon(self.__realpath + "/icons/maximize.svg")

    def get_icon_external_link(self):
        return QtGui.QIcon(self.__realpath + "/icons/external-link.svg")

    # other
    def get_icon_default(self):
        return QtGui.QIcon(self.__realpath + "/icons/default.svg")

    def get_icon_menu(self):
        return QtGui.QIcon(self.__realpath + "/icons/menu.svg")

    def get_icon_facebook(self):
        return QtGui.QIcon(self.__realpath + "/icons/facebook.svg")

    def get_icon_github(self):
        return QtGui.QIcon(self.__realpath + "/icons/facebook.svg")

    def get_icon_vlc(self):
        return QtGui.QIcon(self.__realpath + "/icons/VLC_Icon.svg")

    def get_pixmap_vlc(self):
        return QtGui.QPixmap(self.__realpath + "/icons/VLC_Icon.svg")

    # chevron for combo_box
    def get_icon_chevron_down_24px(self):
        return QtGui.QIcon(self.__realpath + "/icons/chevron-down.svg")

    def get_icon_chevron_down_12px(self):
        return QtGui.QIcon(self.__realpath + "/icons/chevron-down-12.svg")

    def get_icon_chevron_up_24px(self):
        return QtGui.QIcon(self.__realpath + "/icons/chevron-up.svg")

    def get_icon_chevron_up_12px(self):
        return QtGui.QIcon(self.__realpath + "/icons/chevron-up-12.svg")

    # white icon
    def get_icon_chevron_down_white_12px(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-arrow-bottom-12.png")

    def get_icon_chevron_down_white_16px(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-arrow-bottom.png")

    def get_icon_chevron_up_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-arrow-top-12.png")

    def get_icon_camera_roll_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-camera-roll.png")

    def get_icon_check_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-check-alt.png")

    def get_icon_circle_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-circle.png")

    def get_icon_opened_folder_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-folder-open.png")

    def get_icon_loop_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-loop.png")

    def get_icon_loop_circular_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-loop-circular.png")

    def get_icon_pause_video_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-media-pause.png")

    def get_icon_play_video_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-media-play.png")

    def get_icon_rewind_video_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-media-skip-backward.png")

    def get_icon_forward_video_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-media-skip-forward.png")

    def get_icon_menu_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-menu.png")

    def get_icon_cross_x_white(self):
        return QtGui.QIcon(self.__realpath + "/icons/light/cil-x.png")
