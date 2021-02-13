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
from enum import Enum
from typing import List

from dataclasses import dataclass


class DiveMode(Enum):
    OC = 0


class WaterType(Enum):
    Salt = 0
    Fresh = 1


class SoftwareVersion:
    def __init__(self, version: int) -> None:
        self.version: int = version
        self.major: str = f'{int((version / 10000000) % 100)}'
        self.minor: str = f'{int((version / 100000) % 100)}'
        self.patch: str = f'{int((version / 1000) % 100)}'
        self.build: str = f'{version % 1000:03d}'

    @property
    def as_release(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}/{self.build}'

    @property
    def as_numeric(self) -> int:
        return self.version


@dataclass(frozen=True)
class DiveSample:
    vbatCV: float
    runtimeS: int
    depthDm: float
    temperatureDc: float
    activeMixO2Percent: int
    activeMixHePercent: int
    suggestedMixO2Percent: int
    suggestedMixHePercent: int
    activeAlgorithm: int
    buhlGfHigh: int
    buhlGfLow: int
    vpmR0: int
    modeOCSCRCCRGauge: int
    maxPPO2OrSetpoint: int
    firstStopDepth: float
    firstStopTime: int
    NDLOrTTS: int
    OTU: int
    CNS: int
    tissueGroup1Percent: int
    tissueGroup2Percent: int
    tissueGroup3Percent: int
    tissueGroup4Percent: int
    tissueGroup5Percent: int
    tissueGroup6Percent: int
    tissueGroup7Percent: int
    tissueGroup8Percent: int
    tissueGroup9Percent: int
    tissueGroup10Percent: int
    tissueGroup11Percent: int
    tissueGroup12Percent: int
    tissueGroup13Percent: int
    tissueGroup14Percent: int
    tissueGroup15Percent: int
    tissueGroup16Percent: int
    enabledMixSensors: int
    setPointMode: int
    tankPressure: int
    compassLog: int
    reserved2: int


@dataclass(frozen=True)
class Dive:
    activeUser: int
    diveSamples: int
    monotonicTimeS: int
    UTCStartingTimeS: int
    surfacePressureMbar: int
    lastSurfaceTimeS: int
    desaturationTimeS: int
    depthMax: float
    decostopDepth1Dm: float
    decostopDepth2Dm: float
    decostopStep1Dm: int
    decostopStep2Dm: int
    decostopStep3Dm: int
    deepStopAlg: int
    safetyStopDepthDm: float
    safetyStopMin: int
    diveMode: DiveMode
    water: WaterType
    alarmsGeneral: int
    alarmTime: int
    alarmDepth: float
    backlightLevel: int
    backlightMode: int
    softwareVersion: SoftwareVersion
    alertFlag: int
    freeUserSettings: int
    timezoneIdx: int
    avgDepth: float
    dum6: int
    dum7: int
    dum8: int
    samples: List[DiveSample]
