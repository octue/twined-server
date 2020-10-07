import json
import logging
import os
import dramatiq
from django.conf import settings
from octue import Runner
from octue.utils.encoders import OctueJSONEncoder
from reel.messages import ReelMessage


logger = logging.getLogger(__name__)

OUTPUT_STRANDS = ("output_values", "output_manifest")
RUN_STRANDS = ("input_values", "input_manifest", "credentials", "children")


@dramatiq.actor
def asker(analysis_id, **kwargs):
    logger.debug("APPLICATION PATH: %s", settings.APPLICATION_PATH)

    analysis_group_name = f"analysis-{analysis_id}"

    ReelMessage(action="ask", status="started", value=analysis_id).group_send(analysis_group_name)

    # TODO get configuration_values and configuration_manifest out at server start
    logger.debug("SENT MESSAGE TO %s", analysis_group_name)
    try:
        runner = Runner(
            twine=os.path.join(settings.APPLICATION_PATH, "twine.json"),
            configuration_values='{"analysis_program": "kuethe_chow"}',
        )
        # TODO get a log handler and add it to the run
        # TODO get a monitor handler and add it to the run
        analysis = runner.run(app_src=settings.APPLICATION_PATH, **kwargs)
        print("\n\n\nDONE TIH ANALYSIS\n\n\n")

        print("\n\n\nREELING OUTPUTS\n\n\n")
        # TODO fix https://github.com/octue/octue-sdk-python/issues/19 then you can remove this horrifying thing
        kwargs = {}
        for k in OUTPUT_STRANDS:
            att = getattr(analysis, k, None)
            if att is not None:
                att = json.dumps(att, cls=OctueJSONEncoder)

            kwargs[k] = att

        # print('KWARGS', kwargs)
        # print('\n\n\nREELED OUTPUTS\n\n\n')

        # Create the completion message
        ReelMessage(action="ask", status="complete", value=analysis_id, **kwargs).group_send(analysis_group_name)

    except Exception as e:
        print("\n\n\nRAISING REEL ERROR\n\n\n")
        # TODO Except TwinedExceptions and always forward to the client, but any other exceptions only forward if user has admin privilege
        ReelMessage(action="ask", status="error", value=analysis_id, hints=e.args[0]).group_send(analysis_group_name)
        raise e


def ask(analysis_id, message):
    """ Start the ask process
    """

    # Launch the analysis
    kwargs = dict((k, getattr(message, k, None)) for k in RUN_STRANDS)
    asker.send(analysis_id, **kwargs)

    return ReelMessage(action=message.action, reference=message.reference, status="queued", value=analysis_id)
