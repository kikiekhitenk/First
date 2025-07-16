// Enhanced Biomechanical Creature Simulation
// Improved with realistic physics, breathing effects, and lifelike behaviors

var Input = {
  keys: [],
  mouse: {
    left: false,
    right: false,
    middle: false,
    x: 0,
    y: 0,
    prevX: 0,
    prevY: 0
  }
};

// Initialize input arrays
for (var i = 0; i < 230; i++) {
  Input.keys.push(false);
}

// Fixed event listeners with proper comparison operators
document.addEventListener("keydown", function(event) {
  Input.keys[event.keyCode] = true;
});

document.addEventListener("keyup", function(event) {
  Input.keys[event.keyCode] = false;
});

document.addEventListener("mousedown", function(event) {
  if (event.button === 0) {
    Input.mouse.left = true;
  }
  if (event.button === 1) {
    Input.mouse.middle = true;
  }
  if (event.button === 2) {
    Input.mouse.right = true;
  }
});

document.addEventListener("mouseup", function(event) {
  if (event.button === 0) {
    Input.mouse.left = false;
  }
  if (event.button === 1) {
    Input.mouse.middle = false;
  }
  if (event.button === 2) {
    Input.mouse.right = false;
  }
});

document.addEventListener("mousemove", function(event) {
  Input.mouse.prevX = Input.mouse.x;
  Input.mouse.prevY = Input.mouse.y;
  Input.mouse.x = event.clientX;
  Input.mouse.y = event.clientY;
});

// Enhanced Canvas Setup
var canvas = document.createElement("canvas");
document.body.appendChild(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvas.style.position = "absolute";
canvas.style.left = "0px";
canvas.style.top = "0px";
canvas.style.backgroundColor = "#0a0a0a";
document.body.style.overflow = "hidden";
document.body.style.margin = "0";
document.body.style.padding = "0";

var ctx = canvas.getContext("2d");

// Global animation variables
var time = 0;
var breathingPhase = 0;
var ambientNoise = [];

// Initialize ambient noise for organic movement
for (var i = 0; i < 100; i++) {
  ambientNoise.push(Math.random() * 2 - 1);
}

// Enhanced Segment class with organic properties
var segmentCount = 0;
class Segment {
  constructor(parent, size, angle, range, stiffness) {
    segmentCount++;
    this.isSegment = true;
    this.parent = parent;
    if (typeof parent.children == "object") {
      parent.children.push(this);
    }
    this.children = [];
    this.size = size;
    this.originalSize = size;
    this.relAngle = angle;
    this.defAngle = angle;
    this.absAngle = parent.absAngle + angle;
    this.range = range;
    this.stiffness = stiffness;
    this.thickness = Math.max(1, size / 8);
    this.health = 1.0;
    this.tension = 0;
    this.pulse = Math.random() * Math.PI * 2;
    this.breathingOffset = Math.random() * Math.PI * 2;
    this.updateRelative(false, true);
  }

  updateRelative(iter, flex) {
    // Normalize angle
    this.relAngle = this.relAngle - 2 * Math.PI * Math.floor((this.relAngle - this.defAngle) / 2 / Math.PI + 1 / 2);
    
    if (flex) {
      // Enhanced flexibility with organic constraints
      var targetAngle = (this.relAngle - this.defAngle) / this.stiffness + this.defAngle;
      
      // Add subtle breathing motion
      var breathingInfluence = Math.sin(time * 0.05 + this.breathingOffset) * 0.02;
      targetAngle += breathingInfluence;
      
      // Add micro-tremor for realism
      var microTremor = (ambientNoise[segmentCount % ambientNoise.length] * 0.01);
      targetAngle += microTremor;
      
      this.relAngle = Math.min(
        this.defAngle + this.range / 2,
        Math.max(
          this.defAngle - this.range / 2,
          targetAngle
        )
      );
    }
    
    this.absAngle = this.parent.absAngle + this.relAngle;
    
    // Enhanced size calculation with breathing effect
    var breathingFactor = 1 + Math.sin(time * 0.08 + this.breathingOffset) * 0.03;
    this.size = this.originalSize * breathingFactor * this.health;
    
    this.x = this.parent.x + Math.cos(this.absAngle) * this.size;
    this.y = this.parent.y + Math.sin(this.absAngle) * this.size;
    
    // Calculate tension for visual feedback
    this.tension = Math.abs(this.relAngle - this.defAngle) / (this.range / 2);
    
    if (iter) {
      for (var i = 0; i < this.children.length; i++) {
        this.children[i].updateRelative(iter, flex);
      }
    }
  }

  draw(iter) {
    // Enhanced drawing with organic appearance
    var pulseIntensity = Math.sin(time * 0.1 + this.pulse) * 0.3 + 0.7;
    var tensionColor = Math.floor(this.tension * 100 + 100);
    
    // Create gradient based on tension and health
    var gradient = ctx.createLinearGradient(this.parent.x, this.parent.y, this.x, this.y);
    gradient.addColorStop(0, `rgba(${tensionColor}, ${255 - tensionColor}, 150, ${pulseIntensity})`);
    gradient.addColorStop(1, `rgba(${tensionColor + 50}, ${200 - tensionColor}, 180, ${pulseIntensity * 0.8})`);
    
    ctx.strokeStyle = gradient;
    ctx.lineWidth = this.thickness * (0.8 + this.tension * 0.4);
    ctx.lineCap = "round";
    
    // Add shadow for depth
    ctx.shadowColor = "rgba(0, 150, 255, 0.3)";
    ctx.shadowBlur = 3;
    
    ctx.beginPath();
    ctx.moveTo(this.parent.x, this.parent.y);
    ctx.lineTo(this.x, this.y);
    ctx.stroke();
    
    // Draw joint
    ctx.shadowBlur = 0;
    ctx.fillStyle = `rgba(${tensionColor}, ${255 - tensionColor}, 200, ${pulseIntensity})`;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.thickness / 2, 0, Math.PI * 2);
    ctx.fill();
    
    if (iter) {
      for (var i = 0; i < this.children.length; i++) {
        this.children[i].draw(true);
      }
    }
  }

  follow(iter) {
    var x = this.parent.x;
    var y = this.parent.y;
    var dist = Math.sqrt((this.x - x) ** 2 + (this.y - y) ** 2);
    
    if (dist > 0) {
      this.x = x + this.size * (this.x - x) / dist;
      this.y = y + this.size * (this.y - y) / dist;
      this.absAngle = Math.atan2(this.y - y, this.x - x);
      this.relAngle = this.absAngle - this.parent.absAngle;
      this.updateRelative(false, true);
    }
    
    if (iter) {
      for (var i = 0; i < this.children.length; i++) {
        this.children[i].follow(true);
      }
    }
  }
}

// Enhanced LimbSystem with smoother movement
class LimbSystem {
  constructor(end, length, speed, creature) {
    this.end = end;
    this.length = Math.max(1, length);
    this.creature = creature;
    this.speed = speed;
    this.smoothing = 0.1;
    this.targetX = end.x;
    this.targetY = end.y;
    creature.systems.push(this);
    this.nodes = [];
    
    var node = end;
    for (var i = 0; i < length; i++) {
      this.nodes.unshift(node);
      node = node.parent;
      if (!node.isSegment) {
        this.length = i + 1;
        break;
      }
    }
    this.hip = this.nodes[0].parent;
  }

  moveTo(x, y) {
    // Smooth target interpolation
    this.targetX += (x - this.targetX) * this.smoothing;
    this.targetY += (y - this.targetY) * this.smoothing;
    
    this.nodes[0].updateRelative(true, true);
    var dist = Math.sqrt((this.targetX - this.end.x) ** 2 + (this.targetY - this.end.y) ** 2);
    var len = Math.max(0, dist - this.speed);
    
    for (var i = this.nodes.length - 1; i >= 0; i--) {
      var node = this.nodes[i];
      var ang = Math.atan2(node.y - this.targetY, node.x - this.targetX);
      node.x = this.targetX + len * Math.cos(ang);
      node.y = this.targetY + len * Math.sin(ang);
      this.targetX = node.x;
      this.targetY = node.y;
      len = node.size;
    }
    
    for (var i = 0; i < this.nodes.length; i++) {
      var node = this.nodes[i];
      node.absAngle = Math.atan2(node.y - node.parent.y, node.x - node.parent.x);
      node.relAngle = node.absAngle - node.parent.absAngle;
      for (var ii = 0; ii < node.children.length; ii++) {
        var childNode = node.children[ii];
        if (!this.nodes.includes(childNode)) {
          childNode.updateRelative(true, false);
        }
      }
    }
  }

  update() {
    this.moveTo(Input.mouse.x, Input.mouse.y);
  }
}

// Enhanced LegSystem with realistic gait
class LegSystem extends LimbSystem {
  constructor(end, length, speed, creature) {
    super(end, length, speed, creature);
    this.goalX = end.x;
    this.goalY = end.y;
    this.step = 0;
    this.forwardness = 0;
    this.stepHeight = 20;
    this.stepProgress = 0;
    this.gaitPhase = Math.random() * Math.PI * 2;
    
    this.reach = 0.9 * Math.sqrt((this.end.x - this.hip.x) ** 2 + (this.end.y - this.hip.y) ** 2);
    var relAngle = this.creature.absAngle - Math.atan2(this.end.y - this.hip.y, this.end.x - this.hip.x);
    relAngle -= 2 * Math.PI * Math.floor(relAngle / 2 / Math.PI + 1 / 2);
    this.swing = -relAngle + (2 * (relAngle < 0) - 1) * Math.PI / 2;
    this.swingOffset = this.creature.absAngle - this.hip.absAngle;
  }

  update(x, y) {
    // Enhanced stepping with arc motion
    if (this.step == 1) {
      this.stepProgress += 0.15;
      var arcHeight = Math.sin(this.stepProgress * Math.PI) * this.stepHeight;
      var interpX = this.end.x + (this.goalX - this.end.x) * this.stepProgress;
      var interpY = this.end.y + (this.goalY - this.end.y) * this.stepProgress - arcHeight;
      this.moveTo(interpX, interpY);
      
      if (this.stepProgress >= 1) {
        this.step = 0;
        this.stepProgress = 0;
        this.goalX = this.end.x;
        this.goalY = this.end.y;
      }
    } else {
      this.moveTo(this.goalX, this.goalY);
      
      var dist = Math.sqrt((this.end.x - this.goalX) ** 2 + (this.end.y - this.goalY) ** 2);
      var gaitTrigger = Math.sin(time * 0.05 + this.gaitPhase) > 0.3;
      
      if (dist > this.reach * 0.8 && gaitTrigger) {
        this.step = 1;
        this.stepProgress = 0;
        this.goalX = this.hip.x + this.reach * Math.cos(this.swing + this.hip.absAngle + this.swingOffset) + (Math.random() - 0.5) * this.reach * 0.3;
        this.goalY = this.hip.y + this.reach * Math.sin(this.swing + this.hip.absAngle + this.swingOffset) + (Math.random() - 0.5) * this.reach * 0.3;
      }
    }
  }
}

// Enhanced Creature with lifelike behaviors
class Creature {
  constructor(x, y, angle, fAccel, fFric, fRes, fThresh, rAccel, rFric, rRes, rThresh) {
    this.x = x;
    this.y = y;
    this.absAngle = angle;
    this.fSpeed = 0;
    this.fAccel = fAccel;
    this.fFric = fFric;
    this.fRes = fRes;
    this.fThresh = fThresh;
    this.rSpeed = 0;
    this.rAccel = rAccel;
    this.rFric = rFric;
    this.rRes = rRes;
    this.rThresh = rThresh;
    this.children = [];
    this.systems = [];
    this.energy = 1.0;
    this.heartbeat = 0;
    this.size = 6;
    this.breathing = 0;
  }

  follow(x, y) {
    // Enhanced movement with energy system
    var dist = Math.sqrt((this.x - x) ** 2 + (this.y - y) ** 2);
    var angle = Math.atan2(y - this.y, x - this.x);
    
    // Energy-based acceleration
    var accel = this.fAccel * this.energy;
    if (this.systems.length > 0) {
      var groundedLegs = 0;
      for (var i = 0; i < this.systems.length; i++) {
        groundedLegs += this.systems[i].step === 0 ? 1 : 0;
      }
      accel *= groundedLegs / this.systems.length;
    }
    
    this.fSpeed += accel * (dist > this.fThresh);
    this.fSpeed *= 1 - this.fRes;
    this.speed = Math.max(0, this.fSpeed - this.fFric);
    
    // Enhanced rotation with momentum
    var dif = this.absAngle - angle;
    dif -= 2 * Math.PI * Math.floor(dif / (2 * Math.PI) + 1 / 2);
    
    if (Math.abs(dif) > this.rThresh && dist > this.fThresh) {
      this.rSpeed -= this.rAccel * (2 * (dif > 0) - 1) * this.energy;
    }
    
    this.rSpeed *= 1 - this.rRes;
    if (Math.abs(this.rSpeed) > this.rFric) {
      this.rSpeed -= this.rFric * (2 * (this.rSpeed > 0) - 1);
    } else {
      this.rSpeed = 0;
    }
    
    // Update position with micro-adjustments
    this.absAngle += this.rSpeed;
    this.absAngle -= 2 * Math.PI * Math.floor(this.absAngle / (2 * Math.PI) + 1 / 2);
    
    // Add subtle tremor for realism
    var tremor = (Math.random() - 0.5) * 0.02;
    this.x += this.speed * Math.cos(this.absAngle + tremor);
    this.y += this.speed * Math.sin(this.absAngle + tremor);
    
    // Update biological systems
    this.heartbeat += 0.2;
    this.breathing += 0.05;
    this.energy = 0.8 + 0.2 * Math.sin(this.heartbeat);
    
    // Update children
    for (var i = 0; i < this.children.length; i++) {
      this.children[i].updateRelative(true, true);
    }
    
    // Update movement systems
    for (var i = 0; i < this.systems.length; i++) {
      this.systems[i].update(x, y);
    }
    
    this.draw(true);
  }

  draw(iter) {
    // Enhanced creature core with breathing effect
    var breathingSize = this.size * (1 + Math.sin(this.breathing) * 0.1);
    var heartbeatIntensity = Math.sin(this.heartbeat) * 0.5 + 0.5;
    
    // Draw glowing core
    var gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, breathingSize * 2);
    gradient.addColorStop(0, `rgba(100, 200, 255, ${heartbeatIntensity})`);
    gradient.addColorStop(0.7, `rgba(50, 150, 255, ${heartbeatIntensity * 0.5})`);
    gradient.addColorStop(1, 'rgba(0, 100, 200, 0)');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(this.x, this.y, breathingSize * 2, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw creature body
    ctx.strokeStyle = `rgba(150, 200, 255, ${heartbeatIntensity})`;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(this.x, this.y, breathingSize, Math.PI / 4 + this.absAngle, 7 * Math.PI / 4 + this.absAngle);
    
    // Enhanced directional indicator
    var eyeX = this.x + breathingSize * Math.cos(this.absAngle) * 1.5;
    var eyeY = this.y + breathingSize * Math.sin(this.absAngle) * 1.5;
    
    ctx.moveTo(this.x + breathingSize * Math.cos(7 * Math.PI / 4 + this.absAngle), 
               this.y + breathingSize * Math.sin(7 * Math.PI / 4 + this.absAngle));
    ctx.lineTo(eyeX, eyeY);
    ctx.lineTo(this.x + breathingSize * Math.cos(Math.PI / 4 + this.absAngle), 
               this.y + breathingSize * Math.sin(Math.PI / 4 + this.absAngle));
    ctx.stroke();
    
    // Draw eyes
    ctx.fillStyle = `rgba(255, 255, 255, ${heartbeatIntensity})`;
    ctx.beginPath();
    ctx.arc(eyeX, eyeY, 2, 0, Math.PI * 2);
    ctx.fill();
    
    if (iter) {
      for (var i = 0; i < this.children.length; i++) {
        this.children[i].draw(true);
      }
    }
  }
}

// Enhanced setup functions
function setupEnhancedLizard(size, legs, tail) {
  var s = size;
  critter = new Creature(
    window.innerWidth / 2,
    window.innerHeight / 2,
    0,
    s * 8,
    s * 1.5,
    0.3,
    16,
    0.4,
    0.06,
    0.4,
    0.25
  );
  
  var spinal = critter;
  
  // Enhanced neck with more organic movement
  for (var i = 0; i < 6; i++) {
    spinal = new Segment(spinal, s * 4, 0, Math.PI * 2 / 3, 0.8 + i * 0.1);
    
    // Sensory appendages
    for (var ii = -1; ii <= 1; ii += 2) {
      var node = new Segment(spinal, s * 2, ii * 0.8, 0.2, 1.5);
      for (var iii = 0; iii < 2; iii++) {
        node = new Segment(node, s * 1.5, -ii * 0.2, 0.15, 1.8);
      }
    }
  }
  
  // Enhanced body segments with legs
  for (var i = 0; i < legs; i++) {
    if (i > 0) {
      // Spinal segments with breathing motion
      for (var ii = 0; ii < 4; ii++) {
        spinal = new Segment(spinal, s * 3.5, 0, Math.PI / 2, 1.2 + ii * 0.1);
        
        // Breathing ribs
        for (var iii = -1; iii <= 1; iii += 2) {
          var node = new Segment(spinal, s * 2.5, iii * Math.PI / 3, 0.3, 1.2);
          for (var iv = 0; iv < 2; iv++) {
            node = new Segment(node, s * 2, -iii * 0.25, 0.2, 1.5);
          }
        }
      }
    }
    
    // Enhanced legs with realistic joints
    for (var ii = -1; ii <= 1; ii += 2) {
      var hip = new Segment(spinal, s * 8, ii * 0.6, 0.5, 4);
      var thigh = new Segment(hip, s * 12, -ii * 0.6, Math.PI, 0.8);
      var shin = new Segment(thigh, s * 12, ii * 1.2, Math.PI * 0.8, 1.2);
      var foot = new Segment(shin, s * 6, -ii * 0.3, Math.PI / 2, 2);
      
      // Toes for better ground contact
      for (var iii = 0; iii < 3; iii++) {
        new Segment(foot, s * 2, (iii / 2 - 0.5) * 0.8, 0.3, 3);
      }
      
      new LegSystem(foot, 4, s * 8, critter);
    }
  }
  
  // Enhanced tail with tapering segments
  for (var i = 0; i < tail; i++) {
    var taper = (tail - i) / tail;
    spinal = new Segment(spinal, s * 3 * taper, 0, Math.PI / 2 * taper, 0.8 + i * 0.02);
    
    // Tail fins/appendages
    if (i % 3 === 0) {
      for (var ii = -1; ii <= 1; ii += 2) {
        var node = new Segment(spinal, s * 2 * taper, ii * 0.8, 0.4, 1.5);
        node = new Segment(node, s * 1.5 * taper, -ii * 0.3, 0.3, 2);
      }
    }
  }
}

// Enhanced animation loop
function animate() {
  time++;
  
  // Update ambient noise for organic movement
  for (var i = 0; i < ambientNoise.length; i++) {
    ambientNoise[i] += (Math.random() - 0.5) * 0.1;
    ambientNoise[i] *= 0.98; // Decay
    ambientNoise[i] = Math.max(-1, Math.min(1, ambientNoise[i]));
  }
  
  // Clear canvas with fade effect
  ctx.fillStyle = "rgba(10, 10, 10, 0.05)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Draw mouse target
  var mouseGlow = ctx.createRadialGradient(Input.mouse.x, Input.mouse.y, 0, Input.mouse.x, Input.mouse.y, 15);
  mouseGlow.addColorStop(0, 'rgba(255, 100, 100, 0.8)');
  mouseGlow.addColorStop(1, 'rgba(255, 100, 100, 0)');
  ctx.fillStyle = mouseGlow;
  ctx.beginPath();
  ctx.arc(Input.mouse.x, Input.mouse.y, 15, 0, Math.PI * 2);
  ctx.fill();
  
  // Update creature
  if (typeof critter !== 'undefined') {
    critter.follow(Input.mouse.x, Input.mouse.y);
  }
  
  requestAnimationFrame(animate);
}

// Initialize enhanced creature
var critter;
function initialize() {
  var legNum = Math.floor(2 + Math.random() * 8);
  var tailLength = Math.floor(8 + Math.random() * legNum * 4);
  var creatureSize = 12 / Math.sqrt(legNum);
  
  setupEnhancedLizard(creatureSize, legNum, tailLength);
  animate();
}

// Handle window resize
window.addEventListener('resize', function() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

// Start the simulation
initialize();