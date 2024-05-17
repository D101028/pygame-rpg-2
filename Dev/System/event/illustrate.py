#########################################
""" event trigger 說明
    在RPG Maker中，事件（Event）的觸發方式決定了事件在遊戲中如何被激活和執行。以下是每種觸發方式的具體差別：

    1. **Autorun（自動執行）**
        - **描述**：事件會自動開始執行，不需要玩家或其他條件的觸發。
        - **用途**：常用於開場動畫、場景轉換或者其他需要在特定時刻自動執行的事件。
        - **注意**：當一個Autorun事件在運行時，玩家無法進行其他操作，除非事件結束或手動停止。

    2. **Parallel（並行處理）**
        - **描述**：事件會在背景中自動執行，與其他事件或玩家操作並行，不會阻塞玩家的行動。
        - **用途**：適用於需要持續運行或監控的事件，例如計時器、動畫循環、條件檢查等。
        - **注意**：並行事件會消耗一定的系統資源，需注意性能問題。

    3. **Action Button（行動按鈕）**
        - **描述**：事件會在玩家面對事件並按下確認鍵（通常是Z或空格鍵）時觸發。
        - **用途**：適用於互動對話、開關機關、檢查物品等需要玩家主動觸發的事件。
        - **注意**：這是最常見的互動觸發方式，適合大部分需要玩家參與的情境。

    4. **Player Touch（玩家觸碰）**
        - **描述**：當玩家角色移動並碰到事件所在的格子時，事件會被觸發。
        - **用途**：適用於陷阱、觸發區域、即時反應等需要玩家靠近觸發的事件。
        - **注意**：觸發需要玩家移動到特定位置，適合於觸發區域較為明顯的場景。

    5. **Event Touch（事件觸碰）**
        - **描述**：當事件移動並碰到玩家角色時，事件會被觸發。
        - **用途**：適用於敵人接觸戰鬥、追逐劇情等需要事件主動接近玩家的情境。
        - **注意**：此類事件通常需要設置自動移動路徑或AI行動模式。

    總結來說，這些觸發方式提供了不同的事件激活機制，使開發者能夠靈活設計各種互動和劇情發展。選擇合適的觸發方式能夠提升遊戲的整體體驗和流暢度。
"""

# global switches
switches = {
    "first-switch": True
}

# global variables
variables: dict[str, int] = {
    "first-variable": 10
}

"""
    json 格式內呼叫 switch, variable 方法：
        引用變數 "name":
            v[name]
        引用開關 "name":
            s[name]
    json 格式內判斷專門字串
    ex. [pages][][condition] 以及 [pages][][][Conditional Branch][if]
        1. a switch (s[...])
        2. two int with an operator, " " between int and operator, 
        available operator: > = < != ==
            1 == 2
            v[...] == 5

    當事件頁面的條件設置為 "None" 時，該頁面在沒有其他頁面條件被滿足的情況下會自動生效。
"""
# event json format
event_example_format = {
    # these datas won't be saved, and will only be used during the event (only global data will be saved)
    # if global and local variable/switch have the same name, then use the local one.
    "self-switches": {
        "first-self-switch": False
    }, 
    "self-variables": {
        "first-self-variable": 87
    }, 
    "pages": [
        {
            "condition": None, 
            "trigger": "Action Button", 
            "contents": [
                ["Print Test", {
                    "text": "Hello World Page 1"
                }], 
                ["Conditional Branch", {
                    "if": "v[first-self-variable] == 87", 
                    "then": [],  # some contents
                    "else": [],  # some contents
                }], 
                ["Set Variable", {
                    "variable": "first-self-variable", 
                    "value": 78
                }], 
                ["Set Switch", {
                    "variable": "first-self-switch", 
                    "value": True
                }]
            ]
        }, {
            "condition": "v[first-self-variable] < 87", 
            "trigger": "Autorun", 
            "contents": [
                ["Print Test", {
                    "text": "This is page 2"
                }]
            ]
        }
    ]
}

#########################################

