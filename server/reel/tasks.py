import logging
import dramatiq
from django.conf import settings
from reel.messages import ReelMessage


logger = logging.getLogger(__name__)


@dramatiq.actor
def asker(analysis_id, **kwargs):
    logger.debug("APPLICATION PATH: %s", settings.APPLICATION_PATH)

    analysis_group_name = f"analysis-{analysis_id}"

    ReelMessage(action="ask", status="started", value=analysis_id).group_send(analysis_group_name)

    logger.debug("SENT MESSAGE TO %s", analysis_group_name)
    # runner = Runner(
    #     twine=os.path.join(settings.APPLICATION_PATH,'twine.json'),
    #     configuration_values="""{
    #       "width": 600,
    #       "height": 600,
    #       "n_iterations": 64,
    #       "color_scale": "YlGnBu",
    #       "type": "png",
    #       "x_range": [
    #         -1.5,
    #         0.6
    #       ],
    #       "y_range": [
    #         -1.26,
    #         1.26
    #       ]
    #     }
    #     """,
    # )
    # # TODO get a log handler and add it to the run
    # analysis = runner.run(app_src=settings.APPLICATION_PATH, **kwargs)


def ask(analysis_id, message):
    """ Start the ask process
    """

    # Launch the analysis
    RUN_STRANDS = ("input_values", "input_manifest", "credentials", "children")
    kwargs = dict((k, getattr(message, k, None)) for k in RUN_STRANDS)
    asker.send(analysis_id, **kwargs)

    return ReelMessage(action=message.action, reference=message.reference, status="queued", value=analysis_id)
