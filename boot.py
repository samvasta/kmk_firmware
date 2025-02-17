import board

from kmk.bootcfg import bootcfg

bootcfg(
    midi=False,
    mouse=False,
    storage=False,
    usb_id=('Sam Vasta', 'Input 7.4')
)