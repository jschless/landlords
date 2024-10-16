export const test1 = {
    "game_id": "QNGNB",
    "username": "Carrie Holmes",
    "my_cards": [
        3,
        3,
        3,
        4,
        5,
        7,
        8,
        8,
        9,
        9,
        11,
        11,
        12,
        12,
        13,
        13,
        17
    ],
    "players": [
        {
            "username": "Mrs. Julia Bailey",
            "n_cards": 13,
            "exposed_cards": []
        },
        {
            "username": "David Hernandez",
            "n_cards": 12,
            "exposed_cards": [
                4,
                4,
                8
            ]
        }
    ],
    "landlord": 2,
    "landlord_username": "David Hernandez",
    "started": true,
    "action": "update",
    "current_player": 0,
    "current_player_username": "Mrs. Julia Bailey",
    "scoreboard": {
        "Mrs. Julia Bailey": 0,
        "Carrie Holmes": 0,
        "David Hernandez": 0
    },
    "cur_round": [],
    "round_history": [
        [
            [
                "David Hernandez",
                {
                    "base": 3,
                    "chain_length": 2,
                    "low": 5,
                    "kicker_base": 1,
                    "kicker_len": 2,
                    "hand_cards": [
                        5,
                        5,
                        5,
                        6,
                        6,
                        6
                    ],
                    "kicker_cards": [
                        9,
                        12
                    ],
                    "string_repr": "triple-2-chain with 2 single discards"
                }
            ],
            [
                "Mrs. Julia Bailey",
                {
                    "base": 4,
                    "chain_length": 1,
                    "low": 10,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        10,
                        10,
                        10,
                        10
                    ],
                    "kicker_cards": [],
                    "string_repr": "bomb with no discard"
                }
            ]
        ]
    ],
    "bid": 6
};

export const completeGameTestData = {
    "game_id": "CK0BS",
    "username": "Dominic Miller",
    "my_cards": [3,3,4,5,6,7,8,9,10],
    "players": [
        {
            "username": "Carla Munoz",
            "n_cards": 15,
            "exposed_cards": []
        },
        {
            "username": "Jordan Bishop",
            "n_cards": 15,
            "exposed_cards": []
        }
    ],
    "landlord": 0,
    "landlord_username": "Dominic Miller",
    "started": true,
    "action": "update",
    "current_player": 1,
    "current_player_username": "Carla Munoz",
    "scoreboard": {
        "Dominic Miller": 6,
        "Carla Munoz": -3,
        "Jordan Bishop": -3
    },
    "cur_round": [ 
        [
            "Dominic Miller",
            {
                "base": 2,
                "chain_length": 1,
                "low": 6,
                "kicker_base": 0,
                "kicker_len": 0,
                "hand_cards": [
                    6,
                    6
                ],
                "kicker_cards": [],
                "string_repr": "pair-1-chain with no discard"
            }
        ],
        [
            "Carla Munoz",
            {
                "base": 2,
                "chain_length": 1,
                "low": 7,
                "kicker_base": 0,
                "kicker_len": 0,
                "hand_cards": [
                    7,
                    7
                ],
                "kicker_cards": [],
                "string_repr": "pair-1-chain with no discard"
            }
        ]
    ],
    "round_history": [
        [
            [
                "Dominic Miller",
                {
                    "base": 3,
                    "chain_length": 1,
                    "low": 11,
                    "kicker_base": 1,
                    "kicker_len": 1,
                    "hand_cards": [
                        11,
                        11,
                        11
                    ],
                    "kicker_cards": [
                        3
                    ],
                    "string_repr": "triple-1-chain with 1 single discards"
                }
            ]
        ],
        [
            [
                "Dominic Miller",
                {
                    "base": 2,
                    "chain_length": 3,
                    "low": 8,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        8,
                        8,
                        9,
                        9,
                        10,
                        10
                    ],
                    "kicker_cards": [],
                    "string_repr": "pair-3-chain with no discard"
                }
            ]
        ],
        [
            [
                "Dominic Miller",
                {
                    "base": 3,
                    "chain_length": 1,
                    "low": 13,
                    "kicker_base": 2,
                    "kicker_len": 1,
                    "hand_cards": [
                        13,
                        13,
                        13
                    ],
                    "kicker_cards": [
                        4,
                        4
                    ],
                    "string_repr": "triple-1-chain with 1 pair discards"
                }
            ]
        ],
        [
            [
                "Dominic Miller",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 6,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        6,
                        6
                    ],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard"
                }
            ],
            [
                "Carla Munoz",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 7,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        7,
                        7
                    ],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard"
                }
            ],
            [
                "Jordan Bishop",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 12,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        12,
                        12
                    ],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard"
                }
            ],
            [
                "Dominic Miller",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 15,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [
                        15,
                        15
                    ],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard"
                }
            ]
        ]
    ],
    "bid": 3
};

export const ogTestData =  {
    "game_id": "JFV4W",
    "username": "Travis Gregory",
    "my_cards": [
        3,
        3,
        4,
        8,
        9,
        9,
        10,
        10,
        10,
        10,
        12,
        12,
        13,
        14,
        14,
        15,
        15
    ],
    "players": [
        {
            "username": "Sarah Yang",
            "n_cards": 16,
            "exposed_cards": [
                12,
                13,
                15
            ]
        },
        {
            "username": "Calvin Logan",
            "n_cards": 13,
            "exposed_cards": []
        }
    ],
    "landlord": 1,
    "landlord_username": "Sarah Yang",
    "started": true,
    "action": "update",
    "current_player": 1,
    "current_player_username": "Sarah Yang",
    "scoreboard": {
        "Travis Gregory": 0,
        "Sarah Yang": 0,
        "Calvin Logan": 0
    },
    "cur_round": [
        [
            "Papa",
            {
                "base": 3,
                "chain_length": 1,
                "low": 4,
                "kicker_base": 1,
                "kicker_len": 1,
                "hand_cards": [
                    4,
                    4,
                    4
                ],
                "kicker_cards": [
                    3
                ],
                "string_repr": "triple-1-chain with 1 single discards"
            }
        ],
        [
            "Mama",
            {
                "base": 3,
                "chain_length": 1,
                "low": 7,
                "kicker_base": 1,
                "kicker_len": 1,
                "hand_cards": [
                    7,
                    7,
                    7
                ],
                "kicker_cards": [
                    3
                ],
                "string_repr": "triple-1-chain with 1 single discards"
            }
        ]
    ],
    "bid": 3
};
