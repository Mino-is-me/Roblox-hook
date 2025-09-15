-- 로블록스 스튜디오에서 아바타 재구성 스크립트
-- 이 스크립트를 Roblox Studio의 ServerScript에 붙여넣고 실행하세요

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

-- 아바타 타입: R15

local assetIds = {

}

-- 아바타 생성 함수
local function createAvatar()
    local humanoid = workspace:FindFirstChild("Humanoid")
    if not humanoid then
        print("Humanoid not found. Please create a character first.")
        return
    end
    
    -- 아이템 착용
    for _, assetId in pairs(assetIds) do
        local success, result = pcall(function()
            humanoid:AddAccessory(assetId)
        end)
        
        if success then
            print("Added asset: " .. assetId)
        else
            print("Failed to add asset: " .. assetId .. " - " .. tostring(result))
        end
        
        wait(0.1) -- API 제한 방지
    end
end

-- 실행
createAvatar()
print("아바타 재구성 완료!")
