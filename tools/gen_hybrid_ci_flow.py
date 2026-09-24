"""Generate the Hybrid CI flow figure in English and Portuguese.

Drawing both languages from one source keeps them aligned: same geometry,
same palette, only the strings change. Edit CONTENT, run the script from
anywhere, and rebuild the site.
"""

import os
from collections import namedtuple

TEXT = "#545454"
PINK, BLUE, PURPLE = "#ad5e97", "#6975af", "#8f78ad"
PINK_BOX, BLUE_BOX, PURPLE_BOX = "#dcbcd3", "#b9bfda", "#c9bdd9"
PINK_BG, BLUE_BG, PURPLE_BG = "#ebd9e6", "#dbdeec", "#e1d9eb"
FONT = "Open Sans, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"

TITLE_SIZE, BODY_SIZE = 7.6, 5.9
TITLE_LH, BODY_LH = 9.2, 7.2

BOX_W, BOX_H = 106.1, 58.5
ROW_X = [32.5, 162.2, 292.7, 422.9]
PINK_Y, BLUE_Y = 35.1, 187.9
MID_X, MID_W, MID_H = 594.7, 112.4, 59.0
MID_Y = [62.9, 145.8, 228.4]
KERNEL_X, KERNEL_Y, KERNEL_H = 227.9, 262.5, 53.1

PINK_MID = PINK_Y + BOX_H / 2
BLUE_MID = BLUE_Y + BOX_H / 2
MID_CX = MID_X + MID_W / 2

Box = namedtuple("Box", "x y w h fill title body")

CONTENT = {
    "en": {
        "alt": (
            "Hybrid HW/SW continuous integration loop: Processor CI builds the SoC, "
            "a hardware to software handoff regenerates the boot firmware, and Kernel CI "
            "boots Linux and runs the test suites on the board."
        ),
        "title": "Hybrid HW/SW CI loop",
        "lanes": ("PROCESSOR CI", "KERNEL CI", "HW &#8594; SW"),
        "feedback": "FEEDBACK",
        "pink": [
            ("RISC-V Softcore", ["Core RTL + configuration", "and description YAMLs"]),
            ("SoC Generation", ["LiteX assembles interconnect,", "memory and peripherals"]),
            ("Synthesis", ["Vivado synthesizes the SoC", "on a dedicated EDA node"]),
            ("Bitstream +\nMetrics", ["Output"]),
        ],
        "mid": [
            (
                "CSR Map Extraction",
                ["LiteX exports the SoC CSRs", "and peripherals as JSON and CSV"],
            ),
            (
                "Device Tree\nGeneration",
                ["A script converts the map", "into .dts, compiled to .dtb"],
            ),
            (
                "Firmware Build",
                [".dtb is injected into OpenSBI,", "producing updated boot", "firmware"],
            ),
        ],
        "blue": [
            (
                "Dashboard\nSubmission",
                ["UART logs aggregated and", "sent to the public KernelCI", "dashboard"],
            ),
            (
                "Test Execution",
                ["KUnit validates the kernel,", "kselftest validates the", "userspace interface"],
            ),
            (
                "Persistent Runner",
                ["KernelCI monitors the UART;", "the board stays online", "between builds"],
            ),
            (
                "Network Boot",
                ["LiteX BIOS loads OpenSBI,", "Linux and rootfs over TFTP/NFS", "automatically"],
            ),
        ],
        "kernel": "Kernel",
    },
    "pt": {
        "alt": (
            "Laço de integração contínua híbrida de HW e SW: o Processor CI gera o SoC, "
            "a transferência de hardware para software regenera o firmware de boot, e o "
            "Kernel CI inicializa o Linux e roda as suítes de teste na placa."
        ),
        "title": "Laço de CI híbrido de HW/SW",
        "lanes": ("PROCESSOR CI", "KERNEL CI", "HW &#8594; SW"),
        "feedback": "FEEDBACK",
        "pink": [
            ("Softcore RISC-V", ["RTL do core + YAMLs de", "configuração e descrição"]),
            ("Geração do SoC", ["LiteX monta interconexão,", "memória e periféricos"]),
            ("Síntese", ["Vivado sintetiza SoC em nó", "EDA dedicado"]),
            ("Bitstream +\nMétricas", ["Saída"]),
        ],
        "mid": [
            ("Extração do Mapa CSR", ["LiteX exporta CSRs e periféricos", "do SoC em JSON e CSV"]),
            ("Geração da\nDevice Tree", ["Script converte o mapa em .dts,", "compilado para .dtb"]),
            (
                "Compilação do\nFirmware",
                [".dtb é injetado no OpenSBI,", "gerando firmware de boot", "atualizado"],
            ),
        ],
        "blue": [
            (
                "Submissão ao\ndashboard",
                ["logs UART agregados e", "enviados ao dashboard", "público do KernelCI"],
            ),
            (
                "Execução dos testes",
                ["KUnit valida o kernel,", "kselftest valida a interface", "de userspace"],
            ),
            ("Runner persistente", ["KernelCI monitora a UART;", "placa fica online entre builds"]),
            (
                "Boot via Rede",
                ["LiteX BIOS carrega OpenSBI,", "Linux e rootfs via TFTP/NFS", "automaticamente"],
            ),
        ],
        "kernel": "Kernel",
    },
}


def collect_boxes(content):
    """Return every box of the figure, in drawing order."""
    boxes = [
        Box(x, PINK_Y, BOX_W, BOX_H, PINK_BOX, title, body)
        for x, (title, body) in zip(ROW_X, content["pink"])
    ]
    boxes += [
        Box(x, BLUE_Y, BOX_W, BOX_H, BLUE_BOX, title, body)
        for x, (title, body) in zip(ROW_X, content["blue"])
    ]
    boxes += [
        Box(MID_X, y, MID_W, MID_H, PURPLE_BOX, title, body)
        for y, (title, body) in zip(MID_Y, content["mid"])
    ]
    boxes.append(
        Box(KERNEL_X, KERNEL_Y, BOX_W, KERNEL_H, BLUE_BOX, content["kernel"], [])
    )
    return boxes


def render_box(box):
    """Return the rect and the centred lines of text of a single box."""
    cx = box.x + box.w / 2
    titles = box.title.split("\n")
    block = len(titles) * TITLE_LH + len(box.body) * BODY_LH
    cursor = box.y + box.h / 2 - block / 2 + TITLE_SIZE * 0.85
    out = [
        f'  <rect x="{box.x}" y="{box.y}" width="{box.w}" height="{box.h}" '
        f'rx="5.5" fill="{box.fill}"/>'
    ]
    for line in titles:
        out.append(f'  <text x="{cx:.1f}" y="{cursor:.1f}" class="t">{line}</text>')
        cursor += TITLE_LH
    cursor += -TITLE_LH + BODY_LH + 0.6
    for line in box.body:
        out.append(f'  <text x="{cx:.1f}" y="{cursor:.1f}" class="b">{line}</text>')
        cursor += BODY_LH
    return out


def render_defs():
    """Return the gradients, the arrow markers and the stylesheet."""
    out = [
        '  <defs>',
        '    <linearGradient id="pinkToPurple" gradientUnits="userSpaceOnUse" '
        f'x1="531" y1="64" x2="651" y2="64"><stop offset="0" stop-color="{PINK}"/>'
        f'<stop offset="1" stop-color="{PURPLE}"/></linearGradient>',
        '    <linearGradient id="blueToPink" gradientUnits="userSpaceOnUse" '
        f'x1="85.5" y1="188" x2="85.5" y2="94"><stop offset="0" stop-color="{BLUE}"/>'
        f'<stop offset="1" stop-color="{PINK}"/></linearGradient>',
    ]
    for name, color in [("pink", PINK), ("blue", BLUE), ("purple", PURPLE)]:
        out.append(
            f'    <marker id="arrow-{name}" viewBox="0 0 10 10" refX="8.6" refY="5" '
            'markerWidth="5.8" markerHeight="5.8" orient="auto-start-reverse">'
            f'<path d="M 0.6 1 L 9 5 L 0.6 9 z" fill="{color}"/></marker>'
        )
    out += [
        '  </defs>',
        '  <style>',
        f'    text {{ font-family: {FONT}; fill: {TEXT}; text-anchor: middle; }}',
        f'    .t {{ font-size: {TITLE_SIZE}px; font-weight: 700; }}',
        f'    .b {{ font-size: {BODY_SIZE}px; }}',
        '    .lane { font-size: 8px; font-weight: 700; letter-spacing: 0.4px; }',
        '    .fb { font-size: 6.6px; font-weight: 700; }',
        '    .flow { fill: none; stroke-width: 2.1; stroke-linecap: round; '
        'stroke-linejoin: round; }',
        '  </style>',
    ]
    return out


def render_lanes(content):
    """Return the three dashed lanes and their labels."""
    pink_lane, blue_lane, mid_lane = content["lanes"]
    return [
        '  <rect width="750" height="362" fill="#ffffff"/>',
        f'  <rect x="9.7" y="20.8" width="542" height="87.2" rx="7" fill="{PINK_BG}" '
        f'stroke="{PINK}" stroke-width="1.6" stroke-dasharray="7 5"/>',
        f'  <rect x="9.7" y="173.6" width="542" height="155.8" rx="7" fill="{BLUE_BG}" '
        f'stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="7 5"/>',
        f'  <rect x="581.6" y="40.6" width="138.2" height="269.1" rx="7" fill="{PURPLE_BG}" '
        f'stroke="{PURPLE}" stroke-width="1.6" stroke-dasharray="7 5"/>',
        f'  <text x="280.7" y="15.5" class="lane" fill="{PINK}">{pink_lane}</text>',
        f'  <text x="280.7" y="345" class="lane" fill="{BLUE}">{blue_lane}</text>',
        f'  <text x="736" y="175" class="lane" fill="{PURPLE}" '
        f'transform="rotate(90 736 175)">{mid_lane}</text>',
    ]


def render_flows():
    """Return every arrow of the figure."""
    out = []
    for i in range(3):  # processor ci, left to right
        out.append(
            f'  <path class="flow" stroke="{PINK}" marker-end="url(#arrow-pink)" '
            f'd="M {ROW_X[i] + BOX_W + 2.5:.1f} {PINK_MID:.1f} H {ROW_X[i + 1] - 1.5:.1f}"/>'
        )
    for i in range(3):  # kernel ci, right to left
        out.append(
            f'  <path class="flow" stroke="{BLUE}" marker-end="url(#arrow-blue)" '
            f'd="M {ROW_X[i + 1] - 2.5:.1f} {BLUE_MID:.1f} H {ROW_X[i] + BOX_W + 1.5:.1f}"/>'
        )
    for i in range(2):  # hardware to software handoff, top to bottom
        out.append(
            f'  <path class="flow" stroke="{PURPLE}" marker-end="url(#arrow-purple)" '
            f'd="M {MID_CX:.1f} {MID_Y[i] + MID_H + 2.5:.1f} V {MID_Y[i + 1] - 1.5:.1f}"/>'
        )
    out += [
        # bitstream into the handoff column
        '  <path class="flow" stroke="url(#pinkToPurple)" marker-end="url(#arrow-purple)" '
        f'd="M {ROW_X[3] + BOX_W + 2.5:.1f} {PINK_MID:.1f} H 553 C 570 {PINK_MID:.1f} '
        f'568 31 588 31 H 637 C 647 31 {MID_CX:.1f} 36 {MID_CX:.1f} 46 '
        f'V {MID_Y[0] - 1.5:.1f}"/>',
        # firmware back to the board
        f'  <path class="flow" stroke="{PURPLE}" marker-end="url(#arrow-purple)" '
        f'd="M {MID_CX:.1f} {MID_Y[2] + MID_H + 2.5:.1f} V 314 Q {MID_CX:.1f} 325 640 325 '
        f'H 556 Q 545 325 545 314 V 228 Q 545 {BLUE_MID:.1f} 534 {BLUE_MID:.1f} '
        f'H {ROW_X[3] + BOX_W + 1.5:.1f}"/>',
        # dashboard to the kernel and back to the board
        f'  <path class="flow" stroke="{BLUE}" marker-end="url(#arrow-blue)" '
        f'd="M 72 {BLUE_Y + BOX_H + 2.5:.1f} V 278 Q 72 289 83 289 H 224.4"/>',
        f'  <path class="flow" stroke="{BLUE}" marker-end="url(#arrow-blue)" '
        f'd="M 337.5 289 H 465 Q 476 289 476 278 V {BLUE_Y + BOX_H + 1.5:.1f}"/>',
        # test results back to the softcore
        '  <path class="flow" stroke="url(#blueToPink)" marker-end="url(#arrow-pink)" '
        f'd="M 85.5 {BLUE_Y - 2.5:.1f} V {PINK_Y + BOX_H + 1.5:.1f}"/>',
    ]
    return out


def build(lang):
    """Return the complete SVG document for one language."""
    content = CONTENT[lang]
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 362" width="1123" '
        f'height="542" role="img" aria-label="{content["alt"]}">',
        f'  <title>{content["title"]}</title>',
    ]
    svg += render_defs()
    svg += render_lanes(content)
    for box in collect_boxes(content):
        svg += render_box(box)
    svg += render_flows()
    label = content["feedback"]
    svg += [
        f'  <text x="150" y="283" class="fb">{label}</text>',
        f'  <text x="405" y="283" class="fb">{label}</text>',
        f'  <text x="72" y="140" class="fb" transform="rotate(-90 72 140)">{label}</text>',
        '</svg>',
    ]
    return "\n".join(svg) + "\n"


def main():
    """Write both figures under docs/assets/."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for lang in CONTENT:
        path = os.path.join(root, "docs", "assets", f"hybrid_ci_flow_{lang}.svg")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(build(lang))
        print(f"Figura gerada em {os.path.relpath(path, root)}")


if __name__ == "__main__":
    main()
