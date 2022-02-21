""" Autogenerated module for the SHFSG QCodes driver. """
from typing import List, Union
from zhinst.toolkit import CommandTable, Waveforms
from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.qcodes.qcodes_adaptions import ZINode, ZIChannelList


class CommandTableNode(ZINode):
    """CommandTable node.

    This class implements the basic functionality of the command table allowing
    the user to load and upload their own command table.

    A dedicated class called ``CommandTable`` exists that is the prefered way
    to create a valid command table. For more information about the
    ``CommandTable`` refer to the corresponding example or the documentation
    of that class directly.

    Args:
        root: Node used for the upload of the command table
        tree: Tree (node path as tuple) of the current node
        device_type: Device type.
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"commandtable",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

    def check_status(self) -> bool:
        """Check status of the command table.

        Returns:
            Flag if a valid command table is loaded into the device.

        Raises:
            RuntimeError: If the command table upload into the device failed.
        """
        return self._tk_object.check_status()

    def load_validation_schema(self) -> dict:
        """Load device command table validation schema.

        Returns:
            JSON validation schema for the device command tables.
        """
        return self._tk_object.load_validation_schema()

    def upload_to_device(
        self, ct: Union[CommandTable, str, dict], *, validate: bool = True
    ) -> None:
        """Upload command table into the device.

        The command table can either be specified through the dedicated
        ``CommandTable`` class or in a raw format, meaning a json string or json
        dict. In the case of a json string or dict the command table is
        validated by default against the schema provided by the device.

        Args:
            ct: Command table.
            validate: Flag if the command table should be validated. (Only
                applies if the command table is passed as a raw json string or
                json dict)

        Raises:
            RuntimeError: If the command table upload into the device failed.
            zhinst.toolkit.exceptions.ValidationError: Incorrect schema.
        """
        return self._tk_object.upload_to_device(ct=ct, validate=validate)

    def load_from_device(self) -> CommandTable:
        """Load command table from the device.

        Returns:
            command table.
        """
        return self._tk_object.load_from_device()


class AWGCore(ZINode):
    """AWG Core Node"""

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, f"awgcore", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

        if self._tk_object.commandtable:
            submodule = CommandTableNode(
                self,
                "commandtable",
                zi_node="commandtable",
                snapshot_cache=self._snapshot_cache,
            )
            # channel_list.lock()
            self.add_submodule("commandtable", submodule)

    def enable_sequencer(self, *, single: bool) -> None:
        """Starts the sequencer of a specific channel.

        Waits until the sequencer is enabled.

        Args:
            single: Flag if the sequencer should be disabled after finishing
            execution.
        """
        return self._tk_object.enable_sequencer(single=single)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Wait until the AWG is finished.

        Args:
            timeout: The maximum waiting time in seconds for the generator
            (default: 10).
            sleep_time: Time in seconds to wait between requesting generator
            state

        Raises:
            RuntimeError: If continuous mode is enabled
            TimeoutError: If the sequencer program did not finish within the timout
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def load_sequencer_program(
        self, sequencer_program: str, *, timeout: float = 100.0
    ) -> None:
        """Compiles the current SequenceProgram on the AWG Core.

        Args:
            sequencer_program: Sequencer program to be uploaded
            timeout: Maximum time to wait for the compilation on the device in
                seconds. (default = 10s)

        Raises:
            TimeoutError: If the upload or compilation times out.
            RuntimeError: If the upload or compilation failed.
        """
        return self._tk_object.load_sequencer_program(
            sequencer_program=sequencer_program, timeout=timeout
        )

    def write_to_waveform_memory(
        self, waveforms: Waveforms, indexes: list = None
    ) -> None:
        """Writes waveforms to the waveform memory.

        The waveforms must already be assigned in the sequencer programm.

        Args:
            waveforms: Waveforms that should be uploaded.

        Raises:
            IndexError: The index of a waveform exeeds the one on the device
            RuntimeError: One of the waveforms index points to a filler(placeholder)
        """
        return self._tk_object.write_to_waveform_memory(
            waveforms=waveforms, indexes=indexes
        )

    def read_from_waveform_memory(self, indexes: List[int] = None) -> Waveforms:
        """Read waveforms to the waveform memory.

        Args:
            indexes: List of waveform indexes to read from the device. If not
                specfied all assigned waveforms will be downloaded.

        Returns:
            Mutuable mapping of the downloaded waveforms.
        """
        return self._tk_object.read_from_waveform_memory(indexes=indexes)

    def configure_marker_and_trigger(
        self, *, trigger_in_source: str, trigger_in_slope: str, marker_out_source: str
    ) -> None:
        """Configures the trigger inputs and marker outputs of the AWG.

        Args:
            trigger_in_source: alias for the trigger input used by the
                sequencer. For a list of available values use:
                `available_trigger_inputs`
            trigger_in_slope: alias for the slope of the input trigger
                used by sequencer. For a list of available values use
                `available_trigger_inputs`
            marker_out_source: alias for the marker output source used by
                the sequencer. For a list of available values use
                `available_trigger_slopes`
        """
        return self._tk_object.configure_marker_and_trigger(
            trigger_in_source=trigger_in_source,
            trigger_in_slope=trigger_in_slope,
            marker_out_source=marker_out_source,
        )

    @property
    def available_trigger_inputs(self) -> List[str]:
        return self._tk_object.available_trigger_inputs

    @property
    def available_trigger_slopes(self) -> List[str]:
        return self._tk_object.available_trigger_slopes

    @property
    def available_marker_outputs(self) -> List[str]:
        return self._tk_object.available_marker_outputs


class SGChannel(ZINode):
    """Signal Generator Channel for the SHFSG.

    :class:`SGChannel` implements basic functionality to configure SGChannel
    settings of the :class:`SHFSG` instrument.

    Args:
        device: SHFQA device object.
        session: Underlying session.
        tree: tree (node path as tuple) of the coresponding node.
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"sgchannel_{index}",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

        if self._tk_object.awg:

            self.add_submodule(
                "awg",
                AWGCore(
                    self,
                    self._tk_object.awg,
                    zi_node="awg",
                    snapshot_cache=self._snapshot_cache,
                ),
            )

    def configure_channel(
        self, *, enable: bool, output_range: int, center_frequency: float, rf_path: bool
    ) -> None:
        """Configures the RF input and output.

        Args:
            enable: Flag if the signal output should be enabled.
            output_range: maximal range of the signal output power in dbM
            center_frequency: center Frequency before modulation
            rf_path: Flag if the RF(True) or LF(False) path should be
                configured.
        """
        return self._tk_object.configure_channel(
            enable=enable,
            output_range=output_range,
            center_frequency=center_frequency,
            rf_path=rf_path,
        )

    def configure_pulse_modulation(
        self,
        *,
        enable: bool,
        osc_index: int,
        osc_frequency: float = 100000000.0,
        phase: float = 0.0,
        global_amp: float = 0.5,
        gains: tuple = (1.0, -1.0, 1.0, 1.0),
        sine_generator_index: int = 0,
    ) -> None:
        """Configure the pulse modulation.

        Configures the sine generator to digitally modulate the AWG output, for
        generating single sideband AWG signals

        Args:
            enable: Flag if the modulation should be enabled.
            osc_index: selects which oscillator to use
            osc_frequency: oscillator frequency used to modulate the AWG
                outputs. (default = 100e6)
            phase: sets the oscillator phase. (default = 0.0)
            global_amp: global scale factor for the AWG outputs. (default = 0.5)
            gains: sets the four amplitudes used for single sideband generation.
                Default values correspond to upper sideband with a positive
                oscillator frequency. (default = (1.0, -1.0, 1.0, 1.0))
            sine_generator_index: selects which sine generator to use on a
                given channel.
        """
        return self._tk_object.configure_pulse_modulation(
            enable=enable,
            osc_index=osc_index,
            osc_frequency=osc_frequency,
            phase=phase,
            global_amp=global_amp,
            gains=gains,
            sine_generator_index=sine_generator_index,
        )

    def configure_sine_generation(
        self,
        *,
        enable: bool,
        osc_index: int,
        osc_frequency: float = 100000000.0,
        phase: float = 0.0,
        gains: tuple = (0.0, 1.0, 1.0, 0.0),
        sine_generator_index: int = 0,
    ) -> None:
        """Configures the sine generator output.

        Configures the sine generator output of a specified channel for generating
        continuous wave signals without the AWG.

        Args:
            enable: Flag if the sine generator output should be enabled.
            osc_index: selects which oscillator to use
            osc_frequency: oscillator frequency used by the sine generator
                (default = 100e6)
            phase: sets the oscillator phase. (default = 0.0)
            gains: sets the four amplitudes used for single sideband
                generation. default values correspond to upper sideband with a
                positive oscillator frequency. gains are set in this order:
                I/sin, I/cos, Q/sin, Q/cos
                (default = (0.0, 1.0, 1.0, 0.0))
            sine_generator_index: selects which sine generator to use on a given
                channel
        """
        return self._tk_object.configure_sine_generation(
            enable=enable,
            osc_index=osc_index,
            osc_frequency=osc_frequency,
            phase=phase,
            gains=gains,
            sine_generator_index=sine_generator_index,
        )

    @property
    def awg_modulation_freq(self) -> float:
        return self._tk_object.awg_modulation_freq


class SHFSG(ZIBaseInstrument):
    """QCodes driver for the Zurich Instruments SHFSG."""

    def _init_additional_nodes(self):
        """init class specific modules and paramaters."""

        if self._tk_object.sgchannels:

            channel_list = ZIChannelList(
                self,
                "sgchannels",
                SGChannel,
                zi_node="sgchannels",
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.sgchannels):
                channel_list.append(
                    SGChannel(
                        self,
                        x,
                        i,
                        zi_node=f"sgchannels/{i}",
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("sgchannels", channel_list)

    def factory_reset(self, *, deep: bool = True) -> None:
        """Load the factory default settings.

        Args:
            deep: A flag that specifies if a synchronisation
                should be performed between the device and the data
                server after loading the factory preset (default: True).
        """
        return self._tk_object.factory_reset(deep=deep)
