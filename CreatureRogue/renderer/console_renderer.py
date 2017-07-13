import tcod as libtcod


class ConsoleRenderer:
    @staticmethod
    def create_console(title: str, console_width: int, console_height: int, font_file: str, fps_limit: int):
        libtcod.console_set_custom_font(fontFile=font_file, flags=libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(w=console_width, h=console_height, title=title, fullscreen=False)
        libtcod.sys_set_fps(fps_limit)

        return libtcod.console_new(w=console_width, h=console_height)
