
"""

What do I need to do?

- get an application into the container
    - does it need to be built in? Or fetched at start?
    - keep github creds out of it

- configure the application
    - config values + manifest not built into the container
    - read from a mapped drive? use settings with a default to dictate the location of a file or files
    - cache the raw config so it can be used
    - create a twine and configure a Runner
        - does the Runner have to be per-thread? How does that work? Or can I share a runner between consumers?

- map consumers in reel to accept inputs and deliver monitors, outputs
    - create tests for this


conclusions:
    - call 'configure_application(app_path)' as a management command in Reel, so we can configure against
    - repurpose some of the test code (or add a copy_template function for the purpose!) in octue-sdk-python to
      grab application templates and copy to a






"""