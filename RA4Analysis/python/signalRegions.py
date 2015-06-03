# loop looks like this: for njb in signalRegion2fb: for stb in signalRegion2fb[njb]: for htb in signalRegion2fb[njb][stb]: print signalRegion2fb[njb][stb][htb]['deltaPhi']

signalRegion2fb = {(5, 5): {(250, 350): {(500, -1): {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                            (450, -1): {(500, -1): {'deltaPhi': 1.0}}},
                   (6, 7): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                         (750, -1): {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                            (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                        (750, -1): {'deltaPhi': 1.0}}},
                   (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                          (750, -1): {'deltaPhi': 1.0}},
                             (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                             (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                         (750, -1): {'deltaPhi': 1.0}}}
                  }



