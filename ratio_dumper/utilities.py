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
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.cElementTree import Element, SubElement

from crcmod.predefined import mkCrcFun

from .models import Dive


class CrcHelper:
    @staticmethod
    def calculate(payload: bytes) -> int:
        '''Calculate the CRC for a payload in bytes.'''
        return mkCrcFun('crc-ccitt-false')(payload)

    @staticmethod
    def encode(crc: int) -> str:
        '''Bit encode a calculated CRC in 2 bytes.'''
        return f'{(crc >> 8) & 255:02x}{crc & 255:02x}'

    @staticmethod
    def decode(crc_byte1: int, crc_byte2: int) -> int:
        '''Bit decode a calculated CRC in 2 bytes.'''
        return (crc_byte1 << 8) | (crc_byte2 << 0)


class ByteConverter:
    @staticmethod
    def to_int8(data: bytes) -> int:
        """Convert 1 byte into an un-signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_int8 requires one bytes ({data})")
        return data[0]

    @staticmethod
    def to_uint8(data: bytes) -> int:
        """Convert 1 byte into a signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_uint8 requires one bytes ({data})")
        return data[0] & 255

    @staticmethod
    def to_int16(data: bytes) -> int:
        """Convert 2 bytes into a signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_int16 requires two bytes ({data})")
        return (data[1] << 8) | (data[0] & 255)

    @staticmethod
    def to_uint16(data: bytes) -> int:
        """Convert 2 bytes into an un-signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_uint16 requires two bytes ({data})")
        return ((data[1] & 255) << 8) | (data[0] & 255)

    @staticmethod
    def to_int32(data: bytes) -> int:
        """Convert 4 bytes into a signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_int32 requires four bytes ({data})")
        return (data[3] << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))

    @staticmethod
    def to_uint32(data: bytes) -> int:
        """Convert 4 bytes into an un-signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_uint32 requires four bytes ({data})")
        return ((data[3] & 255) << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))


def convert_to_xml(dive: Dive) -> str:
    diveSegment = Element("diveSegment", version="1.1")

    segmentHeader = SubElement(diveSegment, "segmentHeader")
    SubElement(segmentHeader, 'equipmentType').text = '100'
    SubElement(segmentHeader, 'activeUser').text = str(dive.activeUser)
    SubElement(segmentHeader, 'diveSamples').text = str(dive.diveSamples)
    SubElement(segmentHeader, 'monotonicTimeS').text = str(dive.monotonicTimeS)
    SubElement(segmentHeader, 'UTCStartingTimeS').text = str(dive.UTCStartingTimeS)
    SubElement(segmentHeader, 'surfacePressureMbar').text = str(dive.surfacePressureMbar)
    SubElement(segmentHeader, 'lastSurfaceTimeS').text = str(
        dive.lastSurfaceTimeS
        if dive.lastSurfaceTimeS < dive.UTCStartingTimeS else
        -1
    )
    SubElement(segmentHeader, 'desaturationTimeS').text = str(dive.desaturationTimeS)
    SubElement(segmentHeader, 'depthMax').text = str(dive.depthMax)
    SubElement(segmentHeader, 'decostopDepth1Dm').text = str(dive.decostopDepth1Dm)
    SubElement(segmentHeader, 'decostopDepth2Dm').text = str(dive.decostopDepth2Dm)
    SubElement(segmentHeader, 'decostopStep1Dm').text = str(dive.decostopStep1Dm)
    SubElement(segmentHeader, 'decostopStep2Dm').text = str(dive.decostopStep2Dm)
    SubElement(segmentHeader, 'decostopStep3Dm').text = str(dive.decostopStep3Dm)
    SubElement(segmentHeader, 'deepStopAlg').text = str(dive.deepStopAlg)
    SubElement(segmentHeader, 'safetyStopDepthDm').text = str(dive.safetyStopDepthDm)
    SubElement(segmentHeader, 'safetyStopMin').text = str(dive.safetyStopMin)
    SubElement(segmentHeader, 'diveMode').text = str(dive.diveMode)
    SubElement(segmentHeader, 'water').text = str(dive.water)
    SubElement(segmentHeader, 'alarmsGeneral').text = str(dive.alarmsGeneral)
    SubElement(segmentHeader, 'alarmTime').text = str(dive.alarmTime)
    SubElement(segmentHeader, 'alarmDepth').text = str(dive.alarmDepth)
    SubElement(segmentHeader, 'backlightLevel').text = str(dive.backlightLevel)
    SubElement(segmentHeader, 'backlightMode').text = str(dive.backlightMode)
    SubElement(segmentHeader, 'softwareVersion').text = str(dive.softwareVersion)
    SubElement(segmentHeader, 'alertFlag').text = str(dive.alertFlag)
    SubElement(segmentHeader, 'freeUserSettings').text = str(dive.freeUserSettings)
    SubElement(segmentHeader, 'timezoneIdx').text = str(dive.timezoneIdx)
    SubElement(segmentHeader, 'avgDepth').text = str(dive.avgDepth)
    SubElement(segmentHeader, 'dum6').text = str(dive.dum6)
    SubElement(segmentHeader, 'dum7').text = str(dive.dum7)
    SubElement(segmentHeader, 'dum8').text = str(dive.dum8)

    samples = SubElement(diveSegment, "samples")

    for sample in dive.samples:
        diveSample = SubElement(samples, "sample")
        SubElement(diveSample, 'vbatCV').text = str(sample.vbatCV)
        SubElement(diveSample, 'runtimeS').text = str(sample.runtimeS)
        SubElement(diveSample, 'depthDm').text = str(sample.depthDm)
        SubElement(diveSample, 'temperatureDc').text = str(sample.temperatureDc)
        SubElement(diveSample, 'activeMixO2Percent').text = str(sample.activeMixO2Percent)
        SubElement(diveSample, 'activeMixHePercent').text = str(sample.activeMixHePercent)
        SubElement(diveSample, 'suggestedMixO2Percent').text = str(sample.suggestedMixO2Percent)
        SubElement(diveSample, 'suggestedMixHePercent').text = str(sample.suggestedMixHePercent)
        SubElement(diveSample, 'activeAlgorithm').text = str(sample.activeAlgorithm)
        SubElement(diveSample, 'buhlGfHigh').text = str(sample.buhlGfHigh)
        SubElement(diveSample, 'buhlGfLow').text = str(sample.buhlGfLow)
        SubElement(diveSample, 'vpmR0').text = str(sample.vpmR0)
        SubElement(diveSample, 'modeOCSCRCCRGauge').text = str(sample.modeOCSCRCCRGauge)
        SubElement(diveSample, 'maxPPO2OrSetpoint').text = str(sample.maxPPO2OrSetpoint)
        SubElement(diveSample, 'firstStopDepth').text = str(sample.firstStopDepth)
        SubElement(diveSample, 'firstStopTime').text = str(sample.firstStopTime)
        SubElement(diveSample, 'NDLOrTTS').text = str(sample.NDLOrTTS)
        SubElement(diveSample, 'OTU').text = str(sample.OTU)
        SubElement(diveSample, 'CNS').text = str(sample.CNS)
        SubElement(diveSample, 'tissueGroup1Percent').text = str(sample.tissueGroup1Percent)
        SubElement(diveSample, 'tissueGroup2Percent').text = str(sample.tissueGroup2Percent)
        SubElement(diveSample, 'tissueGroup3Percent').text = str(sample.tissueGroup3Percent)
        SubElement(diveSample, 'tissueGroup4Percent').text = str(sample.tissueGroup4Percent)
        SubElement(diveSample, 'tissueGroup5Percent').text = str(sample.tissueGroup5Percent)
        SubElement(diveSample, 'tissueGroup6Percent').text = str(sample.tissueGroup6Percent)
        SubElement(diveSample, 'tissueGroup7Percent').text = str(sample.tissueGroup7Percent)
        SubElement(diveSample, 'tissueGroup8Percent').text = str(sample.tissueGroup8Percent)
        SubElement(diveSample, 'tissueGroup9Percent').text = str(sample.tissueGroup9Percent)
        SubElement(diveSample, 'tissueGroup10Percent').text = str(sample.tissueGroup10Percent)
        SubElement(diveSample, 'tissueGroup11Percent').text = str(sample.tissueGroup11Percent)
        SubElement(diveSample, 'tissueGroup12Percent').text = str(sample.tissueGroup12Percent)
        SubElement(diveSample, 'tissueGroup13Percent').text = str(sample.tissueGroup13Percent)
        SubElement(diveSample, 'tissueGroup14Percent').text = str(sample.tissueGroup14Percent)
        SubElement(diveSample, 'tissueGroup15Percent').text = str(sample.tissueGroup15Percent)
        SubElement(diveSample, 'tissueGroup16Percent').text = str(sample.tissueGroup16Percent)
        SubElement(diveSample, 'enabledMixSensors').text = str(sample.enabledMixSensors)
        SubElement(diveSample, 'setPointMode').text = str(sample.setPointMode)
        SubElement(diveSample, 'tankPressure').text = str(sample.tankPressure)
        SubElement(diveSample, 'compassLog').text = str(sample.compassLog)
        SubElement(diveSample, 'reserved2').text = str(sample.reserved2)

    # Export out the tree as a string
    xmlString = ElementTree.tostring(diveSegment, encoding='utf-8')

    # Re-format our string to be pretty
    return minidom.parseString(xmlString).toprettyxml(encoding='UTF-8',
                                                      indent='    ').decode().strip()
