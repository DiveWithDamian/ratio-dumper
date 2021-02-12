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
from __future__ import annotations

import logging
from io import BytesIO
from types import TracebackType
from typing import Tuple, Set, List, Optional, Type

from serial import Serial

from .models import Dive, DiveSample
from .utilities import ByteConverter, CrcHelper

logger: logging.Logger = logging.getLogger(__name__)


class SerialDriver:
    _serial: Serial

    def __init__(self, serial_path: Optional[str]) -> None:
        # pyre-ignore[16]
        self._serial = Serial(port=serial_path, baudrate=115200, timeout=1)

    def __enter__(self) -> SerialDriver:
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self._serial.close()

    def _encode_payload(self, command: int, options: List[int]) -> bytes:
        '''Encode a set of commands with a CRC.'''
        # Packet layout:
        #  85 = byte, START marker
        #  <variable> = byte, command
        #  <..> = byte, variable length options
        #  <variable> = 2 bytes, CRC of the payload
        payload = f'{85:02x}{len(options) + 1:02x}{command:02x}'
        for option in options:
            payload += f'{option:02x}'
        payload += CrcHelper.encode(CrcHelper.calculate(bytes.fromhex(payload)))
        return bytes.fromhex(payload)

    def _decode_payload(self, command: int) -> Tuple[BytesIO, Optional[int]]:
        '''Decode a response payload.'''
        # Response layout:
        #  85 = byte, START marker
        #  <variable> = byte, command
        #  <variable> = byte, length of payload
        #  <..> = byte, variable length payload
        #  <variable> = byte, ACK or NAK marker
        #  <variable> = 2 bytes, CRC of the payload
        packet_header = self._serial.read(1)
        assert packet_header[0] == 85

        packet_length = self._serial.read(1)
        read_size = int(packet_length.hex(), 16)
        assert read_size > 2 and read_size < 255

        packet_body = self._serial.read(read_size + 2)
        assert len(packet_body) == read_size + 2

        payload, crc = packet_body[:read_size], packet_body[read_size:]
        expected_crc = CrcHelper.calculate(packet_header + packet_length + payload)

        assert expected_crc == CrcHelper.decode(crc[0], crc[1])
        assert payload[0] == command

        # ACK indicates a success
        # Return all data without the command and ack byte
        if payload[-1] == 6:
            return BytesIO(payload[1:-1]), None

        # NAK indicates an error
        # Return the first byte as the error code
        elif payload[-1] == 21:
            return BytesIO(), (payload[1] & 255)

        # Unknown response
        else:
            raise ValueError(f'Unknown response: {payload}')

    def get_dive_ids(self) -> Set[int]:
        '''Query a device for all dives.'''
        self._serial.write(self._encode_payload(120, [141]))
        payload, error_code = self._decode_payload(120)
        if error_code is not None:
            raise RuntimeError(f'get_dive_ids got {error_code}')

        first_dive = ByteConverter.to_uint16(payload.read(2))
        last_dive = ByteConverter.to_uint16(payload.read(2))
        return set(range(first_dive, last_dive + 1))

    def _get_dive_sample(self, sample_id: int) -> DiveSample:
        """Query a device for a specific dive sample."""
        self._serial.write(self._encode_payload(122, [sample_id & 255, (sample_id >> 8) & 255]))
        payload, error_code = self._decode_payload(122)
        if error_code is not None:
            raise RuntimeError(f'get_dive_sample got {error_code}')

        return DiveSample(
            vbatCV=ByteConverter.to_uint16(payload.read(2)),
            runtimeS=ByteConverter.to_uint32(payload.read(4)),
            depthDm=ByteConverter.to_uint16(payload.read(2)),
            temperatureDc=ByteConverter.to_uint16(payload.read(2)),
            activeMixO2Percent=ByteConverter.to_uint8(payload.read(1)),
            activeMixHePercent=ByteConverter.to_uint8(payload.read(1)),
            suggestedMixO2Percent=ByteConverter.to_uint8(payload.read(1)),
            suggestedMixHePercent=ByteConverter.to_uint8(payload.read(1)),
            activeAlgorithm=ByteConverter.to_uint8(payload.read(1)),
            buhlGfHigh=ByteConverter.to_uint8(payload.read(1)),
            buhlGfLow=ByteConverter.to_uint8(payload.read(1)),
            vpmR0=ByteConverter.to_uint8(payload.read(1)),
            modeOCSCRCCRGauge=ByteConverter.to_uint8(payload.read(1)),
            maxPPO2OrSetpoint=ByteConverter.to_uint16(payload.read(2)),
            firstStopDepth=ByteConverter.to_uint16(payload.read(2)),
            firstStopTime=ByteConverter.to_uint16(payload.read(2)),
            NDLOrTTS=ByteConverter.to_uint16(payload.read(2)),
            OTU=ByteConverter.to_uint16(payload.read(2)),
            CNS=ByteConverter.to_uint16(payload.read(2)),
            tissueGroup1Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup2Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup3Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup4Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup5Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup6Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup7Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup8Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup9Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup10Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup11Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup12Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup13Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup14Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup15Percent=ByteConverter.to_uint8(payload.read(1)),
            tissueGroup16Percent=ByteConverter.to_uint8(payload.read(1)),
            enabledMixSensors=ByteConverter.to_uint8(payload.read(1)),
            setPointMode=ByteConverter.to_uint8(payload.read(1)),
            tankPressure=ByteConverter.to_uint8(payload.read(1)),
            compassLog=ByteConverter.to_int16(payload.read(2)),
            reserved2=ByteConverter.to_int16(payload.read(2)),
        )

    def get_dive(self, dive_id: int) -> Dive:
        '''Query a device for a specific dive.'''
        self._serial.write(self._encode_payload(121, [dive_id & 255, (dive_id >> 8) & 255]))
        payload, error_code = self._decode_payload(121)
        if error_code is not None:
            raise RuntimeError(f'get_dive got {error_code}')

        # Decode the segmentHeader
        dive = Dive(
            activeUser=ByteConverter.to_uint8(payload.read(1)),
            diveSamples=ByteConverter.to_uint16(payload.read(2)),
            monotonicTimeS=ByteConverter.to_uint32(payload.read(4)),
            UTCStartingTimeS=ByteConverter.to_uint32(payload.read(4)),
            surfacePressureMbar=ByteConverter.to_uint16(payload.read(2)),
            lastSurfaceTimeS=ByteConverter.to_int32(payload.read(4)),
            desaturationTimeS=ByteConverter.to_int32(payload.read(4)),
            depthMax=ByteConverter.to_uint16(payload.read(2)),
            decostopDepth1Dm=ByteConverter.to_uint16(payload.read(2)),
            decostopDepth2Dm=ByteConverter.to_uint16(payload.read(2)),
            decostopStep1Dm=ByteConverter.to_uint8(payload.read(1)),
            decostopStep2Dm=ByteConverter.to_uint8(payload.read(1)),
            decostopStep3Dm=ByteConverter.to_uint8(payload.read(1)),
            deepStopAlg=ByteConverter.to_uint8(payload.read(1)),
            safetyStopDepthDm=ByteConverter.to_uint8(payload.read(1)),
            safetyStopMin=ByteConverter.to_uint8(payload.read(1)),
            diveMode=ByteConverter.to_uint8(payload.read(1)),
            water=ByteConverter.to_uint8(payload.read(1)),
            alarmsGeneral=ByteConverter.to_uint8(payload.read(1)),
            alarmTime=ByteConverter.to_uint16(payload.read(2)),
            alarmDepth=ByteConverter.to_uint16(payload.read(2)),
            backlightLevel=ByteConverter.to_uint8(payload.read(1)),
            backlightMode=ByteConverter.to_uint8(payload.read(1)),
            softwareVersion=ByteConverter.to_uint32(payload.read(4)),
            alertFlag=ByteConverter.to_uint8(payload.read(1)),
            freeUserSettings=ByteConverter.to_uint8(payload.read(1)),
            timezoneIdx=ByteConverter.to_uint8(payload.read(1)),
            avgDepth=ByteConverter.to_uint16(payload.read(2)),
            dum6=ByteConverter.to_uint8(payload.read(1)),
            dum7=ByteConverter.to_uint8(payload.read(1)),
            dum8=ByteConverter.to_uint8(payload.read(1)),
            samples=[],
        )

        # Decode the samples
        for sample_id in range(1, dive.diveSamples + 1):
            dive.samples.append(self._get_dive_sample(sample_id))

        return dive
