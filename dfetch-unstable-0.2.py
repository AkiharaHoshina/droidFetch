#!/usr/bin/env python3
import os
import sys
import subprocess

# ==========================================
# 0. 帮助说明
# ==========================================
def show_help():
    print("\033[1;32mdroidFetch\033[0m - 专为 Android 环境定制的系统信息展示工具")
    print("")
    print("用法: 可执行文件名(如dfetch.py) [选项]")
    print("")
    print("选项:")
    print("  -h, --help")
    print("     显示此帮助信息并退出")
    print("  -v, --version")
    print("     显示版本信息并退出")
    print("  -T, --tablet")
    print("     启用横屏排版模式 (适合平板或宽屏终端)")
    print("  -D, --custom-distro <ID>")
    print("     调试模式: 强制指定并显示特定的发行版徽标")
    print("  -C, --custom-color <COLOR>")
    print("     调试模式: 强制覆盖主题颜色(支持 ANSI 转义码 或")
    print("     GOOGLE_RAINBOW/PRIDE/TRANS_PRIDE/DEFAULT)")
    print("  --gen-config")
    print("     在 ~/.config/dfetch 下生成默认配置文件 dfetch.conf，并退出")
    print("  --gen-config-samedir")
    print("     在程序同目录的 dfetch 文件夹下生成默认配置文件，供便携测试")
    print("")
    print("发行版 ID 示例:")
    print("  HYPEROS, MIUI, EMUI,")
    print("  COLOROS, ORIGINOS, ONEUI,")
    print("  LINEAGE, PIXELEXP, EVOX,")
    print("  FLYME, NOTHING, PIXEL,")
    print("  CRDROID 等")
    print("")

# ==========================================
# 0.5 配置文件生成与读取逻辑
# ==========================================
def create_config(base_dir):
    """生成默认配置文件并退出"""
    try:
        os.makedirs(base_dir, exist_ok=True)
        conf_path = os.path.join(base_dir, 'dfetch.conf')
        with open(conf_path, 'w', encoding='utf-8') as f:
            f.write("# dfetch 配置文件\n")
            f.write("distro=default\n")
            f.write("color=default\n")
            f.write("custom_ascii=default\n")
            f.write("tablet_mode=default\n")
        print(f"\033[1;32m[+] 配置文件已成功生成: {conf_path}\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[1;31m[-] 配置文件生成失败: {e}\033[0m")
        sys.exit(1)

def load_config():
    """按优先级加载配置文件"""
    home_conf = os.path.expanduser('~/.config/dfetch/dfetch.conf')
    script_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dfetch', 'dfetch.conf')
    
    target_conf = None
    if os.path.isfile(home_conf):
        target_conf = home_conf
    elif os.path.isfile(script_conf):
        target_conf = script_conf
        
    config = {
        'distro': 'default',
        'color': 'default',
        'custom_ascii': 'default',
        'tablet_mode': 'default'
    }
    
    if target_conf:
        try:
            with open(target_conf, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            k, v = line.split('=', 1)
                            config[k.strip()] = v.strip()
        except Exception:
            pass
            
    return config

# ==========================================
# 辅助函数: 获取安卓系统属性
# ==========================================
def getprop(prop_name):
    try:
        result = subprocess.run(['getprop', prop_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""

# ==========================================
# 1. 发行版 (Distro) 深度识别逻辑
# ==========================================
def detect_distro():
    global DISTRO_ID, DISTRO_NAME
    DISTRO_ID = "UNKNOWN"
    DISTRO_NAME = "未知/自定义"
    
    build_id = getprop("ro.build.display.id")
    flavor = getprop("ro.build.flavor")
    incremental = getprop("ro.build.version.incremental")
   
    miui_ver = getprop("ro.miui.ui.version.name")
    if miui_ver:
        if "V816" in miui_ver or "OS1" in incremental:
            DISTRO_ID = "HYPEROS"
            DISTRO_NAME = "Xiaomi HyperOS"
        else:
            DISTRO_ID = "MIUI"
            DISTRO_NAME = f"MIUI {miui_ver}"
        return
    
    if getprop("ro.build.version.emui") or getprop("hw_sc.build.platform.version"):
        DISTRO_ID = "EMUI"
        DISTRO_NAME = "EMUI / HarmonyOS"
        return
    elif getprop("ro.build.version.magic"):
        DISTRO_ID = "MAGICOS"
        DISTRO_NAME = "MagicOS"
        return

    if getprop("ro.build.version.oplusrom") or getprop("ro.oplus.display.version"):
        DISTRO_ID = "COLOROS"
        DISTRO_NAME = "ColorOS / OxygenOS"
        return

    vivo_os_ver = getprop("ro.vivo.os.version")
    vivo_os_name = getprop("ro.vivo.os.name")
    if vivo_os_ver or vivo_os_name:
        DISTRO_ID = "ORIGINOS"
        DISTRO_NAME = f"{vivo_os_name if vivo_os_name else 'OriginOS'} / FuntouchOS"
        return

    oneui_ver = getprop("ro.build.version.oneui")
    if oneui_ver or "One UI" in build_id:
        DISTRO_ID = "ONEUI"
        DISTRO_NAME = f"One UI {oneui_ver}"
        return

    if "Flyme" in build_id or getprop("ro.meizu.setupwizard.flyme"):
        DISTRO_ID = "FLYME"
        DISTRO_NAME = "Flyme OS"
        return

    if getprop("ro.nothing.version.id") or "Nothing" in build_id:
        DISTRO_ID = "NOTHING"
        DISTRO_NAME = "Nothing OS"
        return
    #PIXELXP
    try:
        full_props = subprocess.run(['getprop'], capture_output=True, text=True).stdout
        if "pixelexperience" in full_props.lower():
            DISTRO_ID = "PIXELEXP"
            DISTRO_NAME = "Pixel Experience"
            return
    except Exception:
        pass
    
    if getprop("ro.product.brand").lower() == "google":
        DISTRO_ID = "PIXEL"
        DISTRO_NAME = "Pixel UI"
        return

    if getprop("ro.lineage.build.version") or "lineage" in flavor.lower():
        DISTRO_ID = "LINEAGE"
        DISTRO_NAME = "LineageOS"
        return

    if getprop("ro.evolution.build.version") or "evo" in flavor.lower():
        DISTRO_ID = "EVOX"
        DISTRO_NAME = "Evolution X"
        return

    if getprop("ro.crdroid.build.version") or "crdroid" in flavor.lower():
        DISTRO_ID = "CRDROID"
        DISTRO_NAME = "crDroid"
        return

    if getprop("ro.aospa.version"):
        DISTRO_ID = "AOSPA"
        DISTRO_NAME = "Paranoid Android"
        return

    if "graphene" in flavor.lower() or "graphene" in build_id.lower():
        DISTRO_ID = "GRAPHENE"
        DISTRO_NAME = "GrapheneOS"
        return

    if build_id:
        DISTRO_NAME = f"未知 ({build_id[:15]}...)"

# ==========================================
# 2. 核心渲染与控制引擎
# ==========================================
def main():
    global DISTRO_ID, DISTRO_NAME
    
    # 2.1 参数解析逻辑
    MODE = "vertical"
    FORCE_DISTRO_ID = ""
    FORCE_COLOR = ""  
    cli_tablet_mode = False 
    args = sys.argv[1:]
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help"):
            show_help()
            sys.exit(0)
        elif arg in ("-v", "--version"):
            print("droidFetch version: unstable 0.2 20250520")#版本信息在这里
            sys.exit(0)
        elif arg in ("--gen-config",):
            base_dir = os.path.expanduser('~/.config/dfetch')
            create_config(base_dir)
        elif arg in ("--gen-config-samedir", "gen-config-samedir"):
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dfetch')
            create_config(base_dir)
        elif arg in ("-T", "--tablet"):
            cli_tablet_mode = True 
            i += 1
        elif arg in ("-D", "--custom-distro"):
            if i + 1 < len(args):
                FORCE_DISTRO_ID = args[i + 1]
                i += 2
            else:
                print("\033[1;31m错误: -D/--custom-distro 需要提供一个发行版ID (如 MIUI)\033[0m")
                sys.exit(1)
        elif arg in ("-C", "--custom-color"):
            if i + 1 < len(args):
                FORCE_COLOR = args[i + 1]
                i += 2
            else:
                print("\033[1;31m错误: -C/--custom-color 需要提供一个颜色值\033[0m")
                sys.exit(1)
        else:
            print(f"\033[1;31m未知参数: {arg}\033[0m")
            print("请使用 --help 或者 -h 查看帮助。")
            sys.exit(1)

    # 2.2 执行原生识别逻辑
    detect_distro()
    
    # 读取本地配置
    config_data = load_config()
    conf_distro = config_data.get('distro', 'default')
    conf_color = config_data.get('color', 'default')
    conf_ascii = config_data.get('custom_ascii', 'default')
    conf_tablet = config_data.get('tablet_mode', 'default') 

    if cli_tablet_mode:
        MODE = "horizontal"
    elif conf_tablet.lower() == 'true':
        MODE = "horizontal"
    elif conf_tablet.lower() == 'false':
        MODE = "vertical"

    if conf_distro.lower() != 'default':
        DISTRO_ID = conf_distro.upper()

    if FORCE_DISTRO_ID:
        DISTRO_ID = FORCE_DISTRO_ID.upper()
        DISTRO_NAME = f"[debug] {DISTRO_ID}"

    # 2.3 加载对应徽标与颜色
    logo_dict = {
        "HYPEROS":  (LOGO_HYPEROS, COLOR_HYPEROS),
        "MIUI":     (LOGO_MIUI, COLOR_MIUI),
        "EMUI":     (LOGO_EMUI, COLOR_EMUI),
        "MAGICOS":  (LOGO_MAGICOS, COLOR_MAGICOS),
        "COLOROS":  (LOGO_COLOROS, COLOR_COLOROS),
        "ORIGINOS": (LOGO_ORIGINOS, COLOR_ORIGINOS),
        "ONEUI":    (LOGO_ONEUI, COLOR_ONEUI),
        "FLYME":    (LOGO_FLYME, COLOR_FLYME),
        "NOTHING":  (LOGO_NOTHING, COLOR_NOTHING),
        "PIXEL":    (LOGO_PIXEL, COLOR_PIXEL),
        "PIXELEXP": (LOGO_PIXELEXP, COLOR_PIXELEXP),
        "LINEAGE":  (LOGO_LINEAGE, COLOR_LINEAGE),
        "EVOX":     (LOGO_EVOX, COLOR_EVOX),
        "CRDROID":  (LOGO_CRDROID, COLOR_CRDROID),
        "AOSPA":    (LOGO_AOSPA, COLOR_AOSPA),
        "GRAPHENE": (LOGO_GRAPHENE, COLOR_GRAPHENE)
    }

    rom_logo, rom_color = logo_dict.get(DISTRO_ID, (LOGO_UNKNOWN, COLOR_UNKNOWN))
    
    if conf_ascii.lower() != 'default':
        if os.path.isfile(conf_ascii):
            try:
                with open(conf_ascii, 'r', encoding='utf-8') as f:
                    rom_logo = [line.rstrip('\r\n') for line in f.readlines()]
            except Exception:
                pass

    if FORCE_COLOR:
        FORCE_COLOR = FORCE_COLOR.replace('\\033', '\033').replace('\\e', '\033').replace('\\x1b', '\x1b')
        rom_color = FORCE_COLOR
    elif conf_color.lower() != 'default':
        conf_color = conf_color.replace('\\033', '\033').replace('\\e', '\033').replace('\\x1b', '\x1b')
        rom_color = conf_color

    special_palettes = {
        "GOOGLE_RAINBOW": [
            "\033[38;5;33m",   # Google Blue
            "\033[38;5;196m",  # Google Red
            "\033[38;5;226m",  # Google Yellow
            "\033[38;5;40m",   # Google Green
        ],
        "PRIDE": [
            "\033[38;5;196m",  # Red
            "\033[38;5;208m",  # Orange
            "\033[38;5;226m",  # Yellow
            "\033[38;5;46m",   # Green
            "\033[38;5;27m",   # Blue
            "\033[38;5;93m",   # Purple
        ],
        "TRANS_PRIDE": [
            "\033[38;5;117m",  # Light Blue
            "\033[38;5;211m",  # Pink
            "\033[38;5;231m",  # White
            "\033[38;5;211m",  # Pink
            "\033[38;5;117m",  # Light Blue
        ]
    }

    if not rom_color or rom_color == "DEFAULT":
        rom_color = "\033[1;37m"
        title_color = "\033[1;32m"
    elif rom_color in special_palettes:
        title_color = rom_color
    else:
        title_color = rom_color

    # 2.4 收集系统信息
    brand = getprop("ro.product.brand")
    model = getprop("ro.product.model")
    device = getprop("ro.product.device")
    device_name = f"{brand} {model} ({device})"
    
    os_version = f"Android {getprop('ro.build.version.release')}"
    
    try:
        uname_info = os.uname()
        kernel_version = uname_info.release
        cpu_arch = uname_info.machine
    except Exception:
        kernel_version = "Unknown"
        cpu_arch = "Unknown"
        
    chipset = getprop("ro.board.platform")
    
    try:
        uptime_out = subprocess.run(['uptime', '-p'], capture_output=True, text=True).stdout.strip()
        uptime_info = uptime_out.replace('up ', '', 1)
    except Exception:
        uptime_info = "Unknown"

    mem_total_kb = mem_avail_kb = mem_free_kb = 0
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total_kb = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    mem_avail_kb = int(line.split()[1])
                elif line.startswith("MemFree:"):
                    mem_free_kb = int(line.split()[1])
    except Exception:
        pass
        
    if mem_avail_kb == 0:
        mem_avail_kb = mem_free_kb
        
    mem_used_mb = (mem_total_kb - mem_avail_kb) // 1024
    mem_total_mb = mem_total_kb // 1024

    raw_info = [
        ("设备", device_name),
        ("操作系统", os_version),
        ("发行版", DISTRO_NAME),
        ("内核", kernel_version),
        ("架构", cpu_arch),
        ("芯片组", chipset),
        ("运行时间", uptime_info),
        ("内存", f"{mem_used_mb}MB / {mem_total_mb}MB")
    ]

    info_lines = []
    for idx, (title, value) in enumerate(raw_info):
        if title_color in special_palettes:
            palette = special_palettes[title_color]
            t_color = palette[idx % len(palette)]
        else:
            t_color = title_color
        info_lines.append(f"{t_color}{title}: \033[0m{value}")

    # 2.5 渲染输出 
    android_lines = len(LOGO_ANDROID)
    rom_lines = len(rom_logo)
    info_len = len(info_lines)
    
    max_lines = max(android_lines, rom_lines, info_len)

    # 动态计算左右两部分 ASCII 图案的最大宽度
    # 使用 ljust 可以确保哪怕 custom_ascii 中每行长短不一，右侧面板也能像切豆腐一样整齐对齐
    android_width = max((len(line) for line in LOGO_ANDROID), default=22)
    rom_width = max((len(line) for line in rom_logo), default=14)

    if MODE == "vertical":
        for i in range(max_lines):
            a_line = LOGO_ANDROID[i] if i < android_lines else ""
            r_line = rom_logo[i] if i < rom_lines else ""
            
            if not a_line.strip() and not r_line.strip():
                continue
                
            # 【重构】使用 ljust 将两边对齐，避免塌陷
            a_line_padded = a_line.ljust(android_width)

            if rom_color in special_palettes:
                palette = special_palettes[rom_color]
                current_rom_color = palette[i % len(palette)]
            else:
                current_rom_color = rom_color
                
            print(f"\033[1;32m{a_line_padded}\033[0m{current_rom_color}{r_line}\033[0m")
        print("") 
        for info in info_lines:
            print(info)
            
    else:
        for i in range(max_lines):
            a_line = LOGO_ANDROID[i] if i < android_lines else ""
            r_line = rom_logo[i] if i < rom_lines else ""
            
            # 横屏模式核心修复：将徽标统一填充至其内部最长一行的宽度
            a_line_padded = a_line.ljust(android_width)
            r_line_padded = r_line.ljust(rom_width)
                
            info = info_lines[i] if i < info_len else ""
            
            if rom_color in special_palettes:
                palette = special_palettes[rom_color]
                current_rom_color = palette[i % len(palette)]
            else:
                current_rom_color = rom_color
                
            print(f"\033[1;32m{a_line_padded}\033[0m{current_rom_color}{r_line_padded}\033[0m  {info}")


# ==========================================
# 3. 徽标与颜色库 (ASCII Art & Colors)
# ==========================================
LOGO_ANDROID = [
    "  ;,           ,;     ",
    "   ';,.-----.,;'      ",
    "  ,'           ',     ",
    " /    O     O    \\    ",
    "|                 |   ",
    "'-----------------'   "
]

COLOR_HYPEROS = "\033[38;5;208m"
LOGO_HYPEROS = [
    " Xiaomi HyperOS",
    "    _  .  _    ",
    "   | |.O.| |   ",
    "   | |___| |   ",
    "  /         \\  ",
    " |\\ x     x  | "
]

COLOR_MIUI = "\033[38;5;208m"
LOGO_MIUI = [
    "  Xiaomi MIUI  ",
    "    _     _    ",
    "   | | ★ | |   ",
    "u  | |___| |   ",
    " \\/         \\  ",
    " |  u     u  | "
]

COLOR_EMUI = "\033[1;31m"
LOGO_EMUI = [
"       .##  ##.       ",
"       ###  ###       ",
" ..###  ##  ##  ###.. ",
"   ####  #  #  ####   ",
".##  ### #  # ###  ##.",
"  ###    #  #    ###  ",
"   .=###..  ..###=.   "
]

COLOR_MAGICOS = "\033[1;38;5;27m"
LOGO_MAGICOS = [
    "Honor         ",
    "Magic OS      ",
    "              ",
    "              ",
    "              ",
    "              "
]

COLOR_COLOROS = "\033[1;31m"
LOGO_COLOROS = [
    "          ▄   ",
    "  █▀▀▀▀▀ ▀█▀  ",
    "  █  ◢█   ▄   ",
    "  █  ▄█▄  █   ",
    "  █▄▄▄▄▄▄▄█   "
]

COLOR_ORIGINOS = "\033[1;38;5;197m"
LOGO_ORIGINOS = [
    "         ##   ",
    "   ######     ",
    " ###    ###   ", 
    " ##      ##   ", 
    " ###:   ###   ", 
    "   ######     ",
    "  OriginOS    "  
]

COLOR_ONEUI = "\033[1;34m"
LOGO_ONEUI = [
    "              ",
    "          ✦   ",
    " SAMSUNG ✦    ",
    " Galaxy   ✦   ",
    "              ",
    "              "
]

COLOR_FLYME = "\033[1;37m"
LOGO_FLYME = [
    "              ",
    " Meizu  ✦     ",
    " Flyme AiOS   ",
    "              ",
    "              ",
    "              "
]

COLOR_NOTHING = "\033[1;37m"
LOGO_NOTHING = [
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "  Nothing here."
]

COLOR_PIXEL = "GOOGLE_RAINBOW"
LOGO_PIXEL = [
    "  ▄▄▄▄▄▄  ",
    "  █       ",
    "  █  ▀▀█  ",
    "  █▄▄▄▄█  ",
    "          ",
    "          "
]


COLOR_PIXELEXP = "GOOGLE_RAINBOW"
LOGO_PIXELEXP = [
    "  ▄▄▄▄▄▄  ",
    "  █       ",
    "  █  ▀▀█  ",
    "  █▄▄▄▄█  ",
    "  PixelExperience",
    "          "
]

COLOR_LINEAGE = "\033[38;5;37m"
LOGO_LINEAGE = [
    "              ",
    "            O  ",
    "Lineage OS / \\ ",
    "          O   O",
    "              ",
    "              "
]

COLOR_EVOX = "\x1b[38;5;37m"
LOGO_EVOX = [
"   ---------",
"     ------ ",
"            ",
"   -------- ",
"   -----    ",
"     -----  ",
"       ---  ",
"            ",
" Evolution X"
]

COLOR_CRDROID = "\033[1;37m"
LOGO_CRDROID = [
"       ######       ",
"   ####       ######",
"     #########      ",
" ####    @@     ####",
" ########    ####   ",
"      ###########   ",
" ####      ## ###   ",
"##       ##   ###   ",
"###   ###     ##    ",
" ######      ##     "
]

COLOR_AOSPA = "\x1b[38;5;79m"
LOGO_AOSPA = [
"    --------    ",
"   ----------   ",
"  ------------  ",
"  ----.-..----  ",
" ----.-#...---- ",
" ----.-##-.---- ",
"  ----.--.----  ",
"  ------------  ",
"   ----------   ",
"    --------    "
]

COLOR_GRAPHENE = "\033[1;37m"
LOGO_GRAPHENE = [
"         #         ",
"#        .        #",
"+#    ..###..    #+",
" +#  #       #  #+ ",
"  ###         ###  ",
"   .           .   ",
"   .           .   ",
"  ###         ###  ",
" +#  #..   ..#  #+ ",
"+#      ###      #+",
"#        #        #",
"         #         "
]

COLOR_UNKNOWN = "DEFAULT"
LOGO_UNKNOWN = [
    "              ",
    "Unknown Android",
    "distro or AOSP.",
    "              ",
    "              ",
    "              "
]

# ==========================================
# 4. 执行入口
# ==========================================
if __name__ == "__main__":
    main()