'''
ratio_dumper - Ratio iX5M Log Dumper

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from ratio_dumper import SerialDriver
from tests.utilities import MockSerialIO


def test_get_dive_ids():
    sd = SerialDriver(None)
    sd._serial = MockSerialIO({
        '5502788de20b': '55067801000400064d48',
    })
    assert sd.get_dive_ids() == {1, 2, 3, 4}


def test_get_dive():
    sd = SerialDriver(None)
    sd._serial = MockSerialIO({
        # Get header
        '5503790100c91d': '553879001d008c3602002ac16e186626ffffffff000000007b033c005a003c1e1e00320300010e0000000'
                          '00f0140466402430120d10100000006db4b',
        # Get sample...
        '55037a0100904d': '55c27a7e010a000000130054001500150002501e3200780500000000ff7f00000000000000000000000000'
                          '00000000000000800100000000000100010033cccc336b977e01140000001c0052001500150002501e3200'
                          '780500000000ff7f0000000000000000000000000000000000000000800100000000000200010033cccc33'
                          '055a7e011e000000230050001500150002501e3200780500000000ff7f0000000000000000080817171d1d'
                          '222226262828800100000000000300010033cccc3360bb06af69',
        '55037a0200c51e': '55c27a7e01140000001c0052001500150002501e3200780500000000ff7f00000000000000000000000000'
                          '00000000000000800100000000000200010033cccc33055a7e011e000000230050001500150002501e3200'
                          '780500000000ff7f0000000000000000080817171d1d222226262828800100000000000300010033cccc33'
                          '60bb7e01280000002b0050001500150002501e3200780500000000ff7f0000000000000000080816161c1c'
                          '202024242727800100000000000400010033cccc33568206af69',
        '55037a0300f62f': '55c27a7e011e000000230050001500150002501e3200780500000000ff7f0000000000000000080817171d'
                          '1d222226262828800100000000000300010033cccc3360bb7e01280000002b0050001500150002501e3200'
                          '780500000000ff7f0000000000000000080816161c1c202024242727800100000000000400010033cccc33'
                          '56827d013200000032004f001500150002501e3200780500000000ff7f0000000000000000080815151a1a'
                          '1e1e22222424800100000000000500010033cccc33e31a06af69',
        '55037a04006fb8': '55c27a7e01280000002b0050001500150002501e3200780500000000ff7f0000000000000000080816161c'
                          '1c202024242727800100000000000400010033cccc3356827d013200000032004f001500150002501e3200'
                          '780500000000ff7f0000000000000000080815151a1a1e1e22222424800100000000000500010033cccc33'
                          'e31a7e013c0000003c004e001500150002501e3200780500000000ff7f0000000000000000070713131919'
                          '1c1c20202222800100000000000600010033cccc332fb406af69',
        '55037a05005c89': '55c27a7d013200000032004f001500150002501e3200780500000000ff7f0000000000000000080815151a'
                          '1a1e1e22222424800100000000000500010033cccc33e31a7e013c0000003c004e001500150002501e3200'
                          '780500000000ff7f00000000000000000707131319191c1c20202222800100000000000600010033cccc33'
                          '2fb47e014600000044004e001500150002501e3200780500000000ff7f0000000000000000070712121818'
                          '1b1b1e1e2121800100000000000700010033cccc33c4b706af69',
        '55037a060009da': '55c27a7e013c0000003c004e001500150002501e3200780500000000ff7f00000000000000000707131319'
                          '191c1c20202222800100000000000600010033cccc332fb47e014600000044004e001500150002501e3200'
                          '780500000000ff7f00000000000000000707121218181b1b1e1e2121800100000000000700010033cccc33'
                          'c4b77d01500000004b004d001500150002501e3200780500000000ff7f0000000000000000070711111717'
                          '1a1a1d1d1f1f800100000000000800010033cccc337afd06af69',
        '55037a07003aeb': '55c27a7e014600000044004e001500150002501e3200780500000000ff7f00000000000000000707121218'
                          '181b1b1e1e2121800100000000000700010033cccc33c4b77d01500000004b004d001500150002501e3200'
                          '780500000000ff7f00000000000000000707111117171a1a1d1d1f1f800100000000000800010033cccc33'
                          '7afd7d015a00000053004c001500150002501e3200780500000000ff7f0000000000000000060611111616'
                          '19191b1b1e1e800100000000000900010033cccc33e2bd06af69',
        '55037a08002ad5': '55c27a7d01500000004b004d001500150002501e3200780500000000ff7f00000000000000000707111117'
                          '171a1a1d1d1f1f800100000000000800010033cccc337afd7d015a00000053004c001500150002501e3200'
                          '780500000000ff7f000000000000000006061111161619191b1b1e1e800100000000000900010033cccc33'
                          'e2bd7d016400000057004c001500150002501e3200780500000000ff7f0000000000000000060610101515'
                          '18181b1b1d1d8001001c0000000a00010033cccc33618406af69',
        '55037a090019e4': '55c27a7d015a00000053004c001500150002501e3200780500000000ff7f00000000000000000606111116'
                          '1619191b1b1e1e800100000000000900010033cccc33e2bd7d016400000057004c001500150002501e3200'
                          '780500000000ff7f000000000000000006061010151518181b1b1d1d8001001c0000000a00010033cccc33'
                          '61847d016e00000057004c001500150002501e3200780500000000ff7f0000000000000000060610101515'
                          '18181a1a1d1d8001001c0000000b00010033cccc33e41b06af69',
        '55037a0a004cb7': '55c27a7d016400000057004c001500150002501e3200780500000000ff7f00000000000000000606101015'
                          '1518181b1b1d1d8001001c0000000a00010033cccc3361847d016e00000057004c001500150002501e3200'
                          '780500000000ff7f000000000000000006061010151518181a1a1d1d8001001c0000000b00010033cccc33'
                          'e41b7d017800000057004b001500150002501e3200780500000000ff7f0000000000000000060610101515'
                          '18181b1b1d1d8001001c0000000c00010033cccc33462106af69',
        '55037a0b007f86': '55c27a7d016e00000057004c001500150002501e3200780500000000ff7f00000000000000000606101015'
                          '1518181a1a1d1d8001001c0000000b00010033cccc33e41b7d017800000057004b001500150002501e3200'
                          '780500000000ff7f000000000000000006061010151518181b1b1d1d8001001c0000000c00010033cccc33'
                          '46217d018200000055004b001500150002501e3200780500000000ff7f0000000000000000060611111616'
                          '18181b1b1d1d8001001c0000000d00010033cccc3331c506af69',
        '55037a0c00e611': '55c27a7d017800000057004b001500150002501e3200780500000000ff7f00000000000000000606101015'
                          '1518181b1b1d1d8001001c0000000c00010033cccc3346217d018200000055004b001500150002501e3200'
                          '780500000000ff7f000000000000000006061111161618181b1b1d1d8001001c0000000d00010033cccc33'
                          '31c57d018c00000052004b001500150002501e3200780500000000ff7f0000000000000000060611111616'
                          '18181b1b1e1e8001001c0000000e00010033cccc33d4b306af69',
        '55037a0d00d520': '55c27a7d018200000055004b001500150002501e3200780500000000ff7f00000000000000000606111116'
                          '1618181b1b1d1d8001001c0000000d00010033cccc3331c57d018c00000052004b001500150002501e3200'
                          '780500000000ff7f000000000000000006061111161618181b1b1e1e8001001c0000000e00010033cccc33'
                          'd4b37d01960000004a004b001500150002501e3200780500000000ff7f00000000000000000c0c12121717'
                          '19191c1c1f1f8001001c0000000f00010033cccc33ffe606af69',
        '55037a0e008073': '55c27a7d018c00000052004b001500150002501e3200780500000000ff7f00000000000000000606111116'
                          '1618181b1b1e1e8001001c0000000e00010033cccc33d4b37d01960000004a004b001500150002501e3200'
                          '780500000000ff7f00000000000000000c0c1212171719191c1c1f1f8001001c0000000f00010033cccc33'
                          'ffe67d01a000000042004b001500150002501e3200780500000000ff7f00000000000000000d0d12121818'
                          '1b1b1e1e20208001001c0000001000010033cccc33126e06af69',
        '55037a0f00b342': '55c27a7d01960000004a004b001500150002501e3200780500000000ff7f00000000000000000c0c121217'
                          '1719191c1c1f1f8001001c0000000f00010033cccc33ffe67d01a000000042004b001500150002501e3200'
                          '780500000000ff7f00000000000000000d0d121218181b1b1e1e20208001001c0000001000010033cccc33'
                          '126e7d01aa00000037004b001500150002501e3200780500000000ff7f00000000000000000e0e14141919'
                          '1d1d202022228001001c0000001100010033cccc3357a306af69',
        '55037a1000a00f': '55c27a7d01a000000042004b001500150002501e3200780500000000ff7f00000000000000000d0d121218'
                          '181b1b1e1e20208001001c0000001000010033cccc33126e7d01aa00000037004b001500150002501e3200'
                          '780500000000ff7f00000000000000000e0e141419191d1d202022228001001c0000001100010033cccc33'
                          '57a37d01b400000032004b001500150002501e3200780500000000ff7f00000000000000000f0f15151a1a'
                          '1e1e212124248001001c0000001200010033cccc33835906af69',
        '55037a1100933e': '55c27a7d01aa00000037004b001500150002501e3200780500000000ff7f00000000000000000e0e141419'
                          '191d1d202022228001001c0000001100010033cccc3357a37d01b400000032004b001500150002501e3200'
                          '780500000000ff7f00000000000000000f0f15151a1a1e1e212124248001001c0000001200010033cccc33'
                          '83597c01be00000028004b001500150002501e3200780500000000ff7f0000000000000000101016161c1c'
                          '2020232326268001001c0000001300010033cccc33b19606af69',
        '55037a1200c66d': '55c27a7d01b400000032004b001500150002501e3200780500000000ff7f00000000000000000f0f15151a'
                          '1a1e1e212124248001001c0000001200010033cccc3383597c01be00000028004b001500150002501e3200'
                          '780500000000ff7f0000000000000000101016161c1c2020232326268001001c0000001300010033cccc33'
                          'b1967c01c800000020004b001500150002501e3200780500000000ff7f0000000000000000111118181e1e'
                          '2222262629298001001c0000001400010033cccc33138406af69',
        '55037a1300f55c': '55c27a7c01be00000028004b001500150002501e3200780500000000ff7f0000000000000000101016161c'
                          '1c2020232326268001001c0000001300010033cccc33b1967c01c800000020004b001500150002501e3200'
                          '780500000000ff7f0000000000000000111118181e1e2222262629298001001c0000001400010033cccc33'
                          '13847d01d20000001b004b001500150002501e3200780500000000ff7f0000000000000000121219191f1f'
                          '232327272a2a8001001c0000001500010033cccc33791106af69',
        '55037a14006ccb': '55c27a7c01c800000020004b001500150002501e3200780500000000ff7f0000000000000000111118181e'
                          '1e2222262629298001001c0000001400010033cccc3313847d01d20000001b004b001500150002501e3200'
                          '780500000000ff7f0000000000000000121219191f1f232327272a2a8001001c0000001500010033cccc33'
                          '79117c01dc00000015004b001500150002501e3200780500000000ff7f000000000000000013131b1b2121'
                          '26262a2a2d2d8001001c0000001600010033cccc3342c306af69',
        '55037a15005ffa': '55c27a7d01d20000001b004b001500150002501e3200780500000000ff7f0000000000000000121219191f'
                          '1f232327272a2a8001001c0000001500010033cccc3379117c01dc00000015004b001500150002501e3200'
                          '780500000000ff7f000000000000000013131b1b212126262a2a2d2d8001001c0000001600010033cccc33'
                          '42c37c01e600000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c2222'
                          '27272b2b2f2f8001001c0000001700010033cccc33140306af69',
        '55037a16000aa9': '55c27a7c01dc00000015004b001500150002501e3200780500000000ff7f000000000000000013131b1b21'
                          '2126262a2a2d2d8001001c0000001600010033cccc3342c37c01e600000011004b001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c222227272b2b2f2f8001001c0000001700010033cccc33'
                          '14037c01f000000010004b001500150002501e3200780500000000ff7f000000000000000014141c1c2323'
                          '28282c2c30308001001c0000001800010033cccc33a2bc06af69',
        '55037a17003998': '55c27a7c01e600000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c22'
                          '2227272b2b2f2f8001001c0000001700010033cccc3314037c01f000000010004b001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c232328282c2c30308001001c0000001800010033cccc33'
                          'a2bc7c01fa00000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c2323'
                          '28282c2c2f2f8001001c0000001900010033cccc33f96506af69',
        '55037a180029a6': '55c27a7c01f000000010004b001500150002501e3200780500000000ff7f000000000000000014141c1c23'
                          '2328282c2c30308001001c0000001800010033cccc33a2bc7c01fa00000011004b001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c232328282c2c2f2f8001001c0000001900010033cccc33'
                          'f9657c010401000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c2323'
                          '28282c2c2f2f8001001c0000001a00010033cccc33814b06af69',
        '55037a19001a97': '55c27a7c01fa00000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c23'
                          '2328282c2c2f2f8001001c0000001900010033cccc33f9657c010401000011004b001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c232328282c2c2f2f8001001c0000001a00010033cccc33'
                          '814b7c010e01000010004b001500150002501e3200780500000000ff7f000000000000000014141c1c2323'
                          '28282c2c30308001001c0000001b00010033cccc33da9206af69',
        '55037a1a004fc4': '55c27a7c010401000011004b001500150002501e3200780500000000ff7f000000000000000014141c1c23'
                          '2328282c2c2f2f8001001c0000001a00010033cccc33814b7c010e01000010004b001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c232328282c2c30308001001c0000001b00010033cccc33'
                          'da927b011801000010004a001500150002501e3200780500000000ff7f000000000000000014141c1c2323'
                          '28282c2c30308001001c0000001c00010033cccc335c8206af69',
        '55037a1b007cf5': '55c27a7c010e01000010004b001500150002501e3200780500000000ff7f000000000000000014141c1c23'
                          '2328282c2c30308001001c0000001b00010033cccc33da927b011801000010004a001500150002501e3200'
                          '780500000000ff7f000000000000000014141c1c232328282c2c30308001001c0000001c00010033cccc33'
                          '5c827c01220100000b004a001500150002501e3200780500000000ff7f000000000000000015151d1d2424'
                          '29292d2d31318001001c0000001d00010033cccc33bd4806af69',
        '55037a1c00e562': '55c27a7b011801000010004a001500150002501e3200780500000000ff7f000000000000000014141c1c23'
                          '2328282c2c30308001001c0000001c00010033cccc335c827c01220100000b004a001500150002501e3200'
                          '780500000000ff7f000000000000000015151d1d242429292d2d31318001001c0000001d00010033cccc33'
                          'bd48005c0034050000d68c80181828ffffffff0000000024023c005a003c1e1e00320300010e000000000f'
                          '0140466402400120b80000000000000200aa5555aa3e8406af69',
        '55037a1d00d653': '55c27a7c01220100000b004a001500150002501e3200780500000000ff7f000000000000000015151d1d24'
                          '2429292d2d31318001001c0000001d00010033cccc33bd48005c0034050000d68c80181828ffffffff0000'
                          '000024023c005a003c1e1e00320300010e000000000f0140466402400120b80000000000000200aa5555aa'
                          '3e8485010a000000110046001500150002501e3200780500000000ff7f0000000000000000000000000000'
                          '000000000000800100000000000100020033cccc3371e106af69',
    })
    dive = sd.get_dive(1)

    assert dive.diveSamples == 29
    assert dive.avgDepth == 465
    assert dive.diveMode == 0
    assert dive.UTCStartingTimeS == 409911594
    assert dive.lastSurfaceTimeS == 4294967295
    assert dive.depthMax == 891

    assert dive.samples[0].runtimeS == 10
    assert dive.samples[0].depthDm == 19
    assert dive.samples[0].temperatureDc == 84
    assert dive.samples[0].NDLOrTTS == 32767
