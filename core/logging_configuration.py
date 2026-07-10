import logging

def configure_logging():
#//main logger
    main_logger = logging.getLogger("main")
    main_logger.setLevel(logging.DEBUG)
    main_formatter = logging.Formatter("[MAIN] %(message)s")
    main_handler = logging.StreamHandler()
    main_handler.setFormatter(main_formatter) 
    main_logger.addHandler(main_handler)  

    #//universal logger formating
    universal_tormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    universal_handler = logging.StreamHandler()
    universal_handler.setFormatter(universal_tormatter)

    #//toolbox logger
    toolbox_logger = logging.getLogger("TB")
    toolbox_logger.setLevel(logging.DEBUG)
    toolbox_logger.addHandler(logging.FileHandler("core/logs/toolbox.log"))
    toolbox_logger.addHandler(universal_handler)
    toolbox_logger.propagate = False

    #//tts logger
    #tts_logger = logging.getLogger("TTS")
    #tts_logger.setLevel(logging.DEBUG)
    #tts_logger.addHandler(logging.FileHandler("tts.log"))
    #tts_logger.addHandler(universal_handler)
    #tts_logger.propagate = False

    #//stt logger
    #stt_logger = logging.getLogger("STT")
    #stt_logger.setLevel(logging.DEBUG)
    #stt_logger.addHandler(logging.FileHandler("stt.log"))
    #stt_logger.addHandler(universal_handler)
    #stt_logger.propagate = False

    #//spotify logger
    spotify_logger = logging.getLogger("SP")
    spotify_logger.setLevel(logging.DEBUG)
    spotify_logger.addHandler(logging.FileHandler("core/logs/spotify.log"))
    spotify_logger.addHandler(universal_handler)
    spotify_logger.propagate = False

    #//model logger
    nlp_logger = logging.getLogger("NLP")
    nlp_logger.setLevel(logging.DEBUG)
    nlp_logger.addHandler(logging.FileHandler("core/logs/nlp.log"))
    nlp_logger.addHandler(universal_handler)
    nlp_logger.propagate = False

    #//builtincommands logger
    bic_logger = logging.getLogger("BIC")
    bic_logger.setLevel(logging.DEBUG)
    bic_logger.addHandler(logging.FileHandler("core/logs/bic.log"))
    bic_logger.addHandler(universal_handler)
    bic_logger.propagate = False

    #//builtincommands logger
    session_logger = logging.getLogger("SESSION")
    session_logger.setLevel(logging.DEBUG)
    session_logger.addHandler(logging.FileHandler("core/logs/session.log"))
    session_logger.addHandler(universal_handler)
    session_logger.propagate = False