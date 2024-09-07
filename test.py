class ChatManager :
    def __init__(self, characterDescription):
        self.characterDescription = characterDescription;
        self.messages = [];
    
    def addMessage(role, content) :
        self.messages.push({ role, content });
    
    async getCharacterResponse() :
        return "Character response placeholder"

class Item :
    def __init__(self, name, type, effect):
        self.name = name;
        self.type = type;
        self.effect = effect;

class Ability :
    def __init__(self, name, type, effect, cooldown):
        self.name = name;
        self.type = type;
        self.effect = effect;
        self.cooldown = cooldown;
        self.lastUsed = 0;
    
    def use(user, target) :
        const currentTime = user.scene.time.now
        if currentTime - this.lastUsed >= this.cooldown:
            self.effect(user, target);
            self.lastUsed = currentTime;
            return true
        return false

class Inventory :
    def __init__(self, capacity):
        self.items = [];
        self.capacity = capacity;
        self.equipped = {
        weapon: None,
        armor: None
        }
    
    def addItem(item) :
        if this.items.length < this.capacity:
            self.items.push(item);
            return true
        return false
    
    def removeItem(item) :
        const index = this.items.indexOf(item)
        if index > -1:
            self.items.splice(index, 1);
            return true
        return false
    
    def useItem(item, target) :
        if this.removeItem(item):
            item.effect(target)
            return true
        return false
    
    def equipItem(item) :
        if item.type === 'weapon':
            if this.equipped.weapon:
                self.items.push(self.equipped.weapon);
            self.equipped.weapon = item;
            } else if (item.type === 'armor') {
            if this.equipped.armor:
                self.items.push(self.equipped.armor);
            self.equipped.armor = item;
        self.removeItem(item);

class LightSource :
    def __init__(self, scene, x, y, radius):
        self.scene = scene;
        self.x = x;
        self.y = y;
        self.radius = radius;

class Entity :
    def __init__(self, scene, x, y, char, color = '#ffffff'):
        self.scene = scene;
        self.x = x;
        self.y = y;
        self.char = char;
        self.color = color;
        self.lastMoveTime = 0;
        self.stats = {
        hp:  100,
        maxHp:  100,
        mp:  50,
        maxMp:  50,
        strength:  10,
        dexterity:  10,
        intelligence:  10,
        level:  1,
        movementRate:  1
        }
        self.inventory = new Inventory(10);
        self.abilities = [];
        self.spells = [];
        self.layer = 2; // Default layer for entities
        self.lightSource = null;
    
    def render() :
        self.text = self.scene.add.text(self.x * 20, self.y * 20, self.char, {
        font: '20px monospace',
        fill:  this.color
        })
        self.scene.addToLayer(self.text, self.layer);
        print(`Rendered entity at (${this.x}, ${this.y}) with char ${this.char}`);
    
    def move(dx, dy) :
        const currentTime = this.scene.time.now
        if currentTime - this.lastMoveTime >= 500:
            const newX = this.x + dx
            const newY = this.y + dy
            if this.scene.isWalkable(newX, newY):
                self.x = newX;
                self.y = newY;
                self.text.setPosition(self.x * 20, self.y * 20);
                self.lastMoveTime = currentTime;
                if this.lightSource:
                    self.lightSource.x = self.x;
                    self.lightSource.y = self.y;
                self.scene.updateLineOfSight();
    
    def takeDamage(amount) :
        self.stats.hp = Math.max(0, self.stats.hp - amount);
        if this.stats.hp === 0:
            self.die();
    
    def die() :
        if this instanceof Monster:
            self.scene.dropTreasure(self.x, self.y);
            self.scene.monsters = self.scene.monsters.filter(m => m !== this);
        self.scene.removeFromLayer(self.text, self.layer);
        self.text.destroy();
    
    def useAbility(abilityName, target) :
        const ability = this.abilities.find(a => a.name === abilityName)
        if ability:
            return ability.use(this, target)
        return false
    
    def castSpell(spellName, target) :
        const spell = this.spells.find(s => s.name === spellName)
        if spell && this.stats.mp >= spell.cost:
            self.stats.mp -= spell.cost;
            return spell.use(this, target)
        return false

class Player extends Entity :
    def __init__(self, scene, x, y):
        def super(scene, x, y, '@', '#00ff00');  // Set player color to green
            self.stats.hp = 150;
            self.stats.maxHp = 150;
            self.stats.mp = 100;
            self.stats.maxMp = 100;
            self.weapon = new Item("Sword", "weapon", target => target.takeDamage(10));
            self.armor = new Item("Leather Armor", "armor", wearer => wearer.stats.defense += 5);
            self.inventory.addItem(new Item("Health Potion", "consumable", user => user.stats.hp = Math.min(user.stats.maxHp, user.stats.hp + 50)));
            self.abilities.push(new Ability("Slash", "physical", (user, target) => target.takeDamage(user.stats.strength * 1.5), 2000));
            self.spells.push(new Ability("Fireball", "magical", (user, target) => target.takeDamage(user.stats.intelligence * 2), 5000));
            self.layer = 7; // Player on the new Player layer
            self.lightSource = new LightSource(scene, x, y, 4);
        
        get attackRating() {
        return this.stats.strength + (this.weapon ? this.weapon.effect.damage : 0)
    
    get defenseRating() {
    return this.stats.dexterity + (this.armor ? this.armor.effect.defense : 0)

class Monster extends Entity :
    def __init__(self, scene, x, y, level):
        def super(scene, x, y, '.');
            self.stats.level = level;
            self.updateStats();
            self.updateChar();
            self.abilities.push(new Ability("Bite", "physical", (user, target) => target.takeDamage(user.stats.strength), 3000));
            self.layer = 2; // Monsters on the Entities layer
        
        def updateStats() :
            const levelFactor = this.stats.level - 1
            self.stats.hp = self.stats.maxHp = 50 + levelFactor * 10;
            self.stats.strength = 5 + levelFactor * 2;
            self.stats.dexterity = 5 + levelFactor * 2;
            self.stats.intelligence = 5 + levelFactor * 2;
            self.stats.movementRate = 1 + Math.floor(levelFactor / 3);
        
        def updateChar() :
            const levelDiff = this.stats.level - this.scene.player.stats.level
            if (levelDiff < -1) this.char = '.'
            else if (levelDiff === -1) this.char = 'o'
            else if (levelDiff === 0) this.char = 'O'
            else if (levelDiff === 1) this.char = 'x'
            else if (levelDiff === 2) this.char = 'X'
            else this.char = '#'
            if (this.text) this.text.setText(this.char)
        
        def moveTowardsPlayer() :
            const dx = this.scene.player.x - this.x
            const dy = this.scene.player.y - this.y
            const distance = Math.sqrt(dx * dx + dy * dy)
            
            if distance <= this.stats.movementRate:
                self.move(dx, dy);
                } else {
                const ratio = this.stats.movementRate / distance
                self.move(Math.round(dx * ratio), Math.round(dy * ratio));
    
class GameScene extends Phaser.Scene :
    def __init__(self, ):
        def super('GameScene');
            self.mapWidth = 40;
            self.mapHeight = 25;
            self.inCombat = false;
            self.monsters = [];
            self.debugMode = true;  // Enable debug mode
            self.layers = []; // Array to store layers
            self.layerNames = ['Background', 'Walls', 'Entities', 'Lighting', 'StaticObjects', 'UI', 'Debug', 'Player'];
            self.layerVisibility = [true, true, true, true, true, true, true, true];
            self.torches = [];
        
        def create() :
            print("GameScene create method started");
            self.initializeLayers();
            self.generateMap();
            self.spawnPlayer();
            self.monsters = [];
            for let i = 0,  i < 10,  i++:
                self.addRandomMonster();
            
            self.cursors = self.input.keyboard.createCursorKeys();
            
            self.chatDialogs = new Map();
            
            self.createUI();
            
            self.time.addEvent({
            delay:  2000,
            callback:  this.monsterHeartbeat,
            callbackScope:  this,
            loop:  true
            })
            
            // Debug text
            self.debugText = self.add.text(10, 10, '', { font: '16px Arial', fill: '#ffffff' });
            self.addToLayer(self.debugText, 6);
            
            // Test rendering
            self.testRendering();
            
            // Layer visibility toggles
            self.createLayerToggles();
            
            self.updateLineOfSight();
            
            print("GameScene create method completed");
        
        def initializeLayers() :
            print("Initializing layers");
            for let i = 0,  i < this.layerNames.length,  i++:
                self.layers[i] = self.add.layer();
                self.layers[i].setVisible(self.layerVisibility[i]);
                print(`Layer ${i} (${this.layerNames[i]}) created and set visible: ${this.layerVisibility[i]}`);
        
        def addToLayer(gameObject, layerIndex) :
            if this.layers[layerIndex]:
                self.layers[layerIndex].add(gameObject);
                print(`Added object to layer ${layerIndex} (${this.layerNames[layerIndex]})`);
                } else {
                console.error(`Layer ${layerIndex} does not exist`)
        
        def removeFromLayer(gameObject, layerIndex) :
            if this.layers[layerIndex]:
                self.layers[layerIndex].remove(gameObject);
                } else {
                console.error(`Layer ${layerIndex} does not exist`)
        
        def generateMap() :
            print("Generating map");
            self.map = [];
            for let y = 0,  y < this.mapHeight,  y++:
                let row = []
                for let x = 0,  x < this.mapWidth,  x++:
                    row.append(' '); // Changed from '#' to ' ' to make the area behind walls blank
                self.map.push(row);
            
            // Generate rooms
            const rooms = []
            for let i = 0,  i < 5,  i++:
                const room = this.generateRoom()
                rooms.push(room)
                self.placeRoom(room);
            
            // Connect rooms with hallways
            for let i = 0,  i < rooms.length - 1,  i++:
                self.connectRooms(rooms[i], rooms[i + 1]);
            
            // Place walls around hallways
            self.placeWallsAroundHallways();
            
            // Add torches to rooms
            rooms.forEach(room => {
            if Math.random() < 0.5:
                self.placeTorch(room);
            })
            
            self.updateMapDisplay();
        
        def generateRoom() :
            const width = Phaser.Math.Between(4, 8)
            const height = Phaser.Math.Between(4, 8)
            const x = Phaser.Math.Between(1, this.mapWidth - width - 1)
            const y = Phaser.Math.Between(1, this.mapHeight - height - 1)
            return { x, y, width, height }
        
        def placeRoom(room) :
            for let y = room.y,  y < room.y + room.height,  y++:
                for let x = room.x,  x < room.x + room.width,  x++:
                    if y === room.y || y === room.y + room.height - 1 || x === room.x || x === room.x + room.width - 1:
                        self.map[y][x] = '#';
                        } else {
                        self.map[y][x] = '.';
        
        def connectRooms(room1, room2) :
            let x1 = Phaser.Math.Between(room1.x + 1, room1.x + room1.width - 2)
            let y1 = Phaser.Math.Between(room1.y + 1, room1.y + room1.height - 2)
            let x2 = Phaser.Math.Between(room2.x + 1, room2.x + room2.width - 2)
            let y2 = Phaser.Math.Between(room2.y + 1, room2.y + room2.height - 2)
            
            while x1 !== x2 || y1 !== y2:
                if x1 !== x2:
                    x1 += x1 < x2 ? 1 : -1
                    } else if (y1 !== y2) {
                    y1 += y1 < y2 ? 1 : -1
                if this.map[y1][x1] === '#':
                    self.map[y1][x1] = '+'; // Door
                    } else {
                    self.map[y1][x1] = '.';
        
        def placeWallsAroundHallways() :
            for let y = 1,  y < this.mapHeight - 1,  y++:
                for let x =
                    
                    1; x < this.mapWidth - 1; x++) {
                    if this.map[y][x] === '.':
                        for let dy = -1,  dy <= 1,  dy++:
                            for let dx = -1,  dx <= 1,  dx++:
                                if this.map[y + dy][x + dx] === ' ':
                                    self.map[y + dy][x + dx] = '#';
        
        def placeTorch(room) :
            const x = Phaser.Math.Between(room.x + 1, room.x + room.width - 2)
            const y = Phaser.Math.Between(room.y + 1, room.y + room.height - 2)
            self.map[y][x] = 'T';
            const torch = new LightSource(this, x, y, 3)
            self.torches.push(torch);
        
        def updateMapDisplay() :
            print("Updating map display");
            for let y = 0,  y < this.mapHeight,  y++:
                for let x = 0,  x < this.mapWidth,  x++:
                    const char = this.map[y][x]
                    if char === '#' || char === '+' || char === '.' || char === 'T':
                        text = this.add.text(x * 20, y * 20, char, {
                        font: '20px monospace',
                        fill:  char === '#' ? '#ffffff' :  (char === '+' ? '#8B4513' :  (char === 'T' ? '#FFD700' :  '#666666'))
                        })
                        self.addToLayer(text, 1); // Add walls, doors, floor, and torches to the Walls layer
        
        def spawnPlayer() :
            print("Spawning player");
            let x, y
            do {
            x = Phaser.Math.Between(1, this.mapWidth - 2)
            y = Phaser.Math.Between(1, this.mapHeight - 2)
            } while (!this.isWalkable(x, y))
            
            self.player = new Player(this, x, y);
            self.player.render();
            print(`Player spawned at (${x}, ${y})`);
        
        def addRandomMonster() :
            let x, y
            do {
            x = Phaser.Math.Between(1, this.mapWidth - 2)
            y = Phaser.Math.Between(1, this.mapHeight - 2)
            } while (!this.isWalkable(x, y))
            
            const level = Phaser.Math.Between(this.player.stats.level - 2, this.player.stats.level + 3)
            const monster = new Monster(this, x, y, level)
            monster.render()
            self.monsters.push(monster);
            print(`Monster spawned at (${x}, ${y}) with level ${level}`);
        
        def isWalkable(x, y) :
            return (this.map[y][x] === '.' || this.map[y][x] === '+') &&
            (this.layerVisibility[2] ? !this.monsters.some(m => m.x === x && m.y === y) : true)
        
        def update(time) :
            if !this.inCombat:
                if this.cursors.left.isDown:
                    self.player.move(-1, 0);
                    } else if (this.cursors.right.isDown) {
                    self.player.move(1, 0);
                    } else if (this.cursors.up.isDown) {
                    self.player.move(0, -1);
                    } else if (this.cursors.down.isDown) {
                    self.player.move(0, 1);
                
                self.checkCombat();
            
            // Update monsters
            if this.monsters && Array.isArray(this.monsters):
                self.monsters.forEach(monster => monster.updateChar());
            
            // Update UI
            self.updateUI();
            
            // Update debug information
            self.updateDebugInfo();
        
        def monsterHeartbeat() :
            if !this.inCombat && this.monsters && Array.isArray(this.monsters) && this.layerVisibility[2]:
                self.monsters.forEach(monster => monster.moveTowardsPlayer());
        
        def checkCombat() :
            if this.monsters && Array.isArray(this.monsters) && this.layerVisibility[2]:
                adjacentMonster = this.monsters.find(monster =>
                Math.abs(monster.x - this.player.x) <= 1 &&
                Math.abs(monster.y - this.player.y) <= 1
                )
                
                if adjacentMonster:
                    self.inCombat = true;
                    self.currentMonster = adjacentMonster;
                    self.initiateCombat();
        
        def initiateCombat() :
            print("Combat initiated!");
            self.combatTurn();
        
        def combatTurn() :
            // Player's turn
            const hitRoll = Phaser.Math.Between(1, 20)
            const hitTarget = 10 + this.currentMonster.stats.dexterity
            
            if hitRoll >= hitTarget:
                const damage = this.player.attackRating
                self.currentMonster.takeDamage(damage);
                print(`Player hit! Dealt ${damage} damage.`);
                } else {
                print("Player missed!");
            
            if this.currentMonster.stats.hp > 0:
                // Monster's turn
                const monsterHitRoll = Phaser.Math.Between(1, 20)
                const playerHitTarget = 10 + this.player.stats.dexterity
                
                if monsterHitRoll >= playerHitTarget:
                    const monsterDamage = this.currentMonster.stats.strength
                    self.player.takeDamage(monsterDamage);
                    print(`Monster hit! Dealt ${monsterDamage} damage.`);
                    } else {
                    print("Monster missed!");
                
                // Continue combat
                self.time.delayedCall(1000, self.combatTurn, [], this);
                } else {
                print("Monster defeated!");
                self.endCombat();
        
        def endCombat() :
            self.inCombat = false;
            self.currentMonster = null;
        
        def dropTreasure(x, y) :
            self.map[y][x] = '&';
            treasureText = this.add.text(x * 20, y * 20, '&', {
            font: '20px monospace',
            fill: '#FFD700'  // Set treasure color to gold
            })
            self.addToLayer(treasureText, 4);  // Treasure on StaticObjects layer
        
        def createUI() :
            print("Creating UI");
            self.uiText = self.add.text(810, 10, '', {
            font: '16px monospace',
            fill: '#ffffff',
            wordWrap: { width: 280 }
            })
            self.addToLayer(self.uiText, 5);  // UI layer
            self.updateUI();
        
        def updateUI() :
            if (!this.player) return
            
            const player = this.player
            let inventoryText = 'Inventory:\n'
            if player.inventory && Array.isArray(player.inventory.items):
                player.inventory.items.forEach(item => {
                inventoryText += `- ${item.name}\n`
                })
            
            let equippedText = 'Equipped:\n'
            if (player.inventory.equipped.weapon) equippedText += `Weapon: ${player.inventory.equipped.weapon.name}\n`
            if (player.inventory.equipped.armor) equippedText += `Armor: ${player.inventory.equipped.armor.name}\n`
            
            let abilitiesText = 'Abilities:\n'
            if Array.isArray(player.abilities):
                player.abilities.forEach(ability => {
                abilitiesText += `- ${ability.name}\n`
                })
            
            let spellsText = 'Spells:\n'
            if Array.isArray(player.spells):
                player.spells.forEach(spell => {
                spellsText += `- ${spell.name}\n`
                })
            
            self.uiText.setText(
            `HP: ${player.stats.hp}/${player.stats.maxHp}\n` +
            `MP: ${player.stats.mp}/${player.stats.maxMp}\n` +
            `Level: ${player.stats.level}\n` +
            `Strength: ${player.stats.strength}\n` +
            `Dexterity: ${player.stats.dexterity}\n` +
            `Intelligence: ${player.stats.intelligence}\n` +
            `Attack: ${player.attackRating}\n` +
            `Defense: ${player.defenseRating}\n\n` +
            equippedText + '\n' +
            inventoryText + '\n' +
            abilitiesText + '\n' +
            spellsText
            )
        
        def updateDebugInfo() :
            if (!this.debugMode) return
            
            const visibleElements = this.children.list.filter(child => child.visible).length
            const totalElements = this.children.list.length
            
            self.debugText.setText(
            `Debug Mode: ON\n` +
            `Player Position: (${this.player.x}, ${this.player.y})\n` +
            `Visible Elements: ${visibleElements}/${totalElements}\n` +
            `Monsters: ${this.monsters.length}\n` +
            `Layer Visibility: ${this.layerVisibility.map((v, i) => `${this.layerNames[i]}: ${v}`).join(', ')}`
            )
        
        def testRendering() :
            print("Testing rendering");
            // Add a red rectangle
            const rect = this.add.rectangle(400, 300, 100, 100, 0xff0000)
            self.addToLayer(rect, 6);
            
            // Add some text
            text = this.add.text(400, 200, 'Test Rendering', {
            font: '32px Arial',
            fill: '#00ff00'
            })
            text.setOrigin(0.5)
            self.addToLayer(text, 6);
            
            print("Test rendering objects added");
        
        def createLayerToggles() :
            const toggleBox = this.add.rectangle(1000, 300, 180, 200, 0x333333)
            self.addToLayer(toggleBox, 6);
            
            const title = this.add.text(920, 210, 'Layer Visibility', { font: '18px Arial', fill: '#ffffff' })
            self.addToLayer(title, 6);
            
            self.layerCheckboxes = [];
            
            for let i = 0,  i < this.layers.length,  i++:
                const y = 240 + i * 30
                const checkbox = this.add.rectangle(930, y, 20, 20, 0xffffff)
                self.addToLayer(checkbox, 6);
                
                const label = this.add.text(960, y - 10, this.layerNames[i], { font: '16px Arial', fill: '#ffffff' })
                self.addToLayer(label, 6);
                
                checkbox.setInteractive()
                checkbox.on('pointerdown', () => {
                self.layerVisibility[i] = !self.layerVisibility[i];
                self.layers[i].setVisible(self.layerVisibility[i]);
                checkbox.fillColor = this.layerVisibility[i] ? 0x00ff00 : 0xff0000
                })
                
                // Set initial state
                checkbox.fillColor = this.layerVisibility[i] ? 0x00ff00 : 0xff0000
                self.layerCheckboxes.push(checkbox);
        
        def updateLayerToggles() :
            for let i = 0,  i < this.layers.length,  i++:
                self.layerCheckboxes[i].fillColor = self.layerVisibility[i] ? 0x00ff00 : 0xff0000;
        
        def updateLineOfSight() :
            if (!this.player) return
            
            // Clear previous line of sight and light
            if this.lineOfSightGraphics:
                self.lineOfSightGraphics.clear();
                } else {
                self.lineOfSightGraphics = self.add.graphics();
                self.addToLayer(self.lineOfSightGraphics, 3); // Add to Lighting layer
            
            const playerX = this.player.x
            const playerY = this.player.y
            
            // Combine player's light source with wall torches
            const lightSources = [this.player.lightSource, ...this.torches]
            
            for let y = 0,  y < this.mapHeight,  y++:
                for let x = 0,  x < this.mapWidth,  x++:
                    if this.hasLineOfSight(playerX, playerY, x, y):
                        let maxIntensity = 0
                        
                        // Check all light sources
                        for const lightSource of lightSources:
                            const dx = x - lightSource.x
                            const dy = y - lightSource.y
                            const distance = Math.sqrt(dx * dx + dy * dy)
                            
                            if distance <= lightSource.radius:
                                // Calculate light intensity based on distance
                                const intensity = 1 - (distance / lightSource.radius)
                                maxIntensity = Math.max(maxIntensity, intensity)
                        
                        if maxIntensity > 0:
                            const alpha = 0.3 * maxIntensity
                            // Apply yellow light where line of sight and any light source radius overlap
                            self.lineOfSightGraphics.fillStyle(0xffff00, alpha);
                            self.lineOfSightGraphics.fillRect(x * 20, y * 20, 20, 20);
        
        def hasLineOfSight(x1, y1, x2, y2) :
            const dx = Math.abs(x2 - x1)
            const dy = Math.abs(y2 - y1)
            const sx = x1 < x2 ? 1 : -1
            const sy = y1 < y2 ? 1 : -1
            let err = dx - dy
            
            while true:
                if (x1 === x2 && y1 === y2) return true
                if (this.map[y1][x1] === '#') return false
                
                const e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
    
    config = {
    type:  Phaser.AUTO,
    width:  1100,
    height:  600,
    scene:  GameScene,
    parent: 'renderDiv',
    pixelArt:  true,
    backgroundColor: '#000000',
    physics: {
    default: 'arcade',
    arcade: {
    debug:  false
}

window.phaserGame = new Phaser.Game(config)

// Add error logging
window.onerror =

def function(message, source, lineno, colno, error) :
console.error('An error occurred:', message, 'at', source, 'line', lineno)
return false
}