import tcod as libtcod


class ConsoleRenderer:
    @staticmethod
    def create_console(title: str, console_width: int, console_height: int, font_file: str, fps_limit: int):
        libtcod.console.set_custom_font(fontFile=font_file, flags=libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console.init_root(w=console_width, h=console_height, title=title, fullscreen=False)
        libtcod.sys.set_fps(fps_limit)

        return libtcod.console.new(w=console_width, h=console_height)
