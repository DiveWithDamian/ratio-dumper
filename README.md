Ratio iX5M Log Dumper
=====================

Python dumper for the Ratio iX5M (iX3M 2021, square buttons/latest firmware).

## Example usage

```python3
from ratio_dumper import SerialDriver, convert_to_xml

with SerialDriver('/dev/tty.usbserial-D309VENO') as dc:
    dive = dc.get_dive(1)
    print(convert_to_xml(dive))
```

## Support Notes

The majority of testing has been done against open circuit dive logs from a iX5M computer,
little support exists for CCR specific data e.g. setpoints, cell calibration etc.

## Implementation references

- https://github.com/subsurface/libdc
- http://www.ratio-computers.com/toolbox/Ratio_Toolbox_Mac.zip
- https://github.com/aeruder/slsnif
