#pftypes = ["X", "h", "e", "mu", "gamma", "h0", "h_HF", "egamma_HF"]
label = {"X":0,"h":1, "e":2, "mu":3,"gamma":4, 'h0':5, 'h_HF':6, 'egamma_HF':7, 0:"X",1:"h", 2:"e", 3:"mu",4:"gamma", 5:'h0', 6:'h_HF', 7:'egamma_HF'}

categories = {\
  "gamma":[ ["gamma_mE", -99, -1.4  ],
            ["gamma_mB", -1.4, 0.   ],
            ["gamma_pB", 0., 1.4    ],
            ["gamma_pE", 1.4, 99    ]],
  "h":[ ["h_mE", -99., -1.5  ],
        ["h_mB", -1.5, 0.   ],
        ["h_pB", 0., 1.5    ],
        ["h_pE", 1.5, 99    ]],
  'h0':[["h0_mE", -99, -1.4  ],
        ["h0_mB", -1.4, 0.   ],
        ["h0_pB", 0., 1.4    ],
        ["h0_pE", 1.4, 99    ]],
  'h_HF':[["h_HF_m", -99., 0.],
          ["h_HF_p", 0., 99.]],
  'egamma_HF':[["egamma_HF_m", -99., 0.],
               ["egamma_HF_p", 0., 99.]]
}

