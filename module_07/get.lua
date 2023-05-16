local frandom = io.open("/dev/urandom", "rb")
local d = frandom:read(4)
math.randomseed(d:byte(1) + (d:byte(2) * 256) + (d:byte(3) * 65536) + (d:byte(4) * 4294967296))

local file = io.open("oids.txt", "r");
local oids = {}
for line in file:lines() do
    table.insert (oids, line);
end

request = function()
    headers = {}
    number =  math.random(1,100000)
    headers["Content-Type"] = "application/json"
    body = ''
    return wrk.format("GET", "/authors/".. oids[number], headers, body)
end
