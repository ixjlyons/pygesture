------------------------------------------------------------------------------ 
-- Following few lines automatically added by V-REP to guarantee compatibility 
-- with V-REP 3.1.3 and earlier: 
colorCorrectionFunction=function(_aShapeHandle_) 
	local version=simGetIntegerParameter(sim_intparam_program_version) 
	local revision=simGetIntegerParameter(sim_intparam_program_revision) 
	if (version<30104)and(revision<3) then 
		return _aShapeHandle_ 
	end 
	return '@backCompatibility1:'.._aShapeHandle_ 
end 
------------------------------------------------------------------------------ 


lockMcp = function(finger)
	-- locks MCP joint in its current position
	simSetObjectIntParameter(jointHandles[finger][2], 2001, 1)
	simSetJointForce(jointHandles[finger][2], closingOpeningTorque*100)
	simSetJointTargetPosition(
			jointHandles[finger][2], 
			simGetJointPosition(jointHandles[finger][2]))
end

unlockMcp = function(finger, velocity)
	-- unlocks MCP joint and starts opening it
	simSetObjectIntParameter(jointHandles[finger][2], 2001, 0)
	simSetJointForce(jointHandles[finger][2], closingOpeningTorque)
	simSetJointTargetVelocity(jointHandles[finger][2], velocity)
end

moveFinger = function(finger, velocity)
	simSetJointTargetVelocity(jointHandles[finger][2], velocity)
	simSetJointTargetPosition(
			jointHandles[finger][3], 
			(45*math.pi/180)+simGetJointPosition(jointHandles[finger][2])/3)
end

attachCup = function()
	simSetObjectParent(cupHandle, connector, true)
	simSetShapeColor(colorCorrectionFunction(indicatorHandle), '',
			sim_colorcomponent_ambient, indicatorColors[2])
end

detachCup = function()
	simSetObjectParent(cupHandle, -1, true)
	simSetShapeColor(colorCorrectionFunction(indicatorHandle), '',
			sim_colorcomponent_ambient, indicatorColors[1])
end


if (sim_call_type == sim_childscriptcall_initialization) then

	----------------
	-- parameters --
	----------------
	mcpTorqueOvershootCountRequired = 1
	mcpMaxTorque = 0.9
	closingVel = 60*math.pi/180
	openingVel = -120*math.pi/180
	closingOpeningTorque = 1
	ipFullyOpenPosition = 45.5*math.pi/180
	mcpFullyOpenPosition = 0.5*math.pi/180
	
	indicatorColors = {{0, 0, 0}, {0, 0.8, 0.8}}


	-- assuming right hand
	jointHandles = {
		{-1, -1, -1}, -- right finger : separator, MCP, PIP
		{-1, -1, -1}, -- thumb        : N/A,       MCP, IP
		{-1, -1, -1}  -- left finger  : separator, MCP, PIP
	}
	mcpTorqueSensorHandles = {-1,-1,-1} -- MCP joints

	for i = 0, 2, 1 do
		if (i ~= 1) then
			jointHandles[i+1][1] = simGetObjectHandle('BarrettHand_jointA_'..i)
		end
		jointHandles[i+1][2] = simGetObjectHandle('BarrettHand_jointB_'..i)
		jointHandles[i+1][3] = simGetObjectHandle('BarrettHand_jointC_'..i)
		mcpTorqueSensorHandles[i+1] = simGetObjectHandle('BarrettHand_jointB_'..i)
	end
	
	connector = simGetObjectHandle('BarrettHand_attachPoint')
	objectSensor = simGetObjectHandle('BarrettHand_attachProxSensor')
	cupHandle = simGetObjectHandle('Cup')
	indicatorHandle = simGetObjectHandle('Disc')

	modelHandle = simGetObjectAssociatedWithScript(sim_handle_self)
	ui = simGetUIHandle('BarrettHand')
	simSetUIButtonLabel(ui, 0, simGetObjectName(modelHandle))
	closing = false
	mcpLocked = {false, false, false}
	
	mcpTorqueOvershootCount = {0, 0, 0}
	
	-- 0: finger can open or close freely
	-- 1: finger has "overtorqued" and needs to fully open before closing
	-- 2: finger is fully opening
	needFullOpening = {0, 0, 0}

	req = 0

	for i = 1, 3, 1 do
		-- enable MCP dynamic motor
		simSetObjectIntParameter(jointHandles[i][2], 2000, 1)
		-- disable MCP dynamic motor control loop
		simSetObjectIntParameter(jointHandles[i][2], 2001, 0)
		-- enable IP dynamic motor
		simSetObjectIntParameter(jointHandles[i][3], 2000, 1)
		-- enable IP dynamic motor control loop
		simSetObjectIntParameter(jointHandles[i][3], 2001, 1)

		simSetJointTargetVelocity(jointHandles[i][2], 0)
		simSetJointTargetVelocity(jointHandles[i][3], 0)
		simSetJointForce(jointHandles[i][2], closingOpeningTorque)
		simSetJointForce(jointHandles[i][3], closingOpeningTorque)
	end

	-- fix "finger separator" joints
	simSetJointTargetPosition(jointHandles[1][1], -90)
	simSetJointTargetPosition(jointHandles[3][1], -90)
	
	detachCup()
end 


if (sim_call_type == sim_childscriptcall_cleanup) then 
	for i = 1, 3, 1 do
		simSetObjectIntParameter(jointHandles[i][2], 2000, 1)
		simSetObjectIntParameter(jointHandles[i][2], 2001, 0)
		simSetObjectIntParameter(jointHandles[i][3], 2000, 1)
		simSetObjectIntParameter(jointHandles[i][3], 2001, 1)
		simSetJointTargetVelocity(jointHandles[i][2], 0)
		simSetJointTargetVelocity(jointHandles[i][3], 0)
		simSetJointForce(jointHandles[i][2], closingOpeningTorque)
		simSetJointForce(jointHandles[i][3], closingOpeningTorque)
	end
	detachCup()
end


if (sim_call_type == sim_childscriptcall_actuation) then 
	
	-- check for request from remote API
	req = simGetIntegerSignal("request")
	-- req == 0: rest
	-- req == 1: close fist
	-- req == 2: open hand
	if (req) then
		simClearStringSignal("request")
		if (req == 0) then
			--closing = false
		elseif (req == 1) then
			closing = true
		else
			closing = false
		end
	else
		closing = false
	end

	-- actuate each of the three fingers
	for i = 1, 3, 1 do
		if (closing) and 
				(needFullOpening[1] ~= 2) and
				(needFullOpening[2] ~= 2) and
				(needFullOpening[3] ~= 2) then
			
			if (mcpLocked[i]) then
				simSetJointTargetVelocity(jointHandles[i][3], closingVel/3)
			else
				-- check MCP torque
				t = simJointGetForce(mcpTorqueSensorHandles[i])
				if (t) and (t < -mcpMaxTorque) then
					mcpTorqueOvershootCount[i] = mcpTorqueOvershootCount[i] + 1
				else
					mcpTorqueOvershootCount[i] = 0
				end
				
				if (mcpTorqueOvershootCount[i] < mcpTorqueOvershootCountRequired) then
					moveFinger(i, closingVel)
				else
					needFullOpening[i] = 1
					mcpLocked[i] = true
					lockMcp(i)
					-- disable PIP motor control loop (disable position control)
					simSetObjectIntParameter(jointHandles[i][3], 2001, 0)
					simSetJointTargetVelocity(jointHandles[i][3], closingVel/3)
				end
			end
		else
			if (needFullOpening[i] == 1) then
				needFullOpening[i] = 2
			end

			simSetJointTargetVelocity(jointHandles[i][3], openingVel/3)

			if (mcpLocked[i]) then
				ipPosition = simGetJointPosition(jointHandles[i][3])
				if (ipPosition < ipFullyOpenPosition) then
					mcpLocked[i] = false
					unlockMcp(i, openingVel)
				end
			else
				if (needFullOpening[i] ~= 0) then
					ipPosition = simGetJointPosition(jointHandles[i][3])
					mcpPosition = simGetJointPosition(jointHandles[i][2])
					if (ipPosition < ipFullyOpenPosition) and
							(mcpPosition < mcpFullyOpenPosition) then
						needFullOpening[i] = 0
						-- enable PIP motor control loop (position control)
						simSetObjectIntParameter(jointHandles[i][3], 2001, 1)
						simSetJointTargetPosition(jointHandles[i][3], (45*math.pi/180) + 
								simGetJointPosition(jointHandles[i][2])/3)
					end
				else
					moveFinger(openingVel)
				end
			end
		end
	end
end


if (sim_call_type == sim_childscriptcall_sensing) then
	-- attach the object if the thumb and at least one finger are grasping
	if (mcpLocked[1] and mcpLocked[2]) or (mcpLocked[3] and mcpLocked[1]) then
		attachCup()
	else
		detachCup()
	end
end
