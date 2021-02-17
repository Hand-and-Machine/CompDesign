import Turtle.*;

Turtle t;

// list of instruction characters
char[] alphabet = {'F','+','-'};

// substitution rules for the instruction characters
String[] substitutions = {"F+F-F+F+F","+","-"};

// initial set of instructions
String instructions = "F";
int instrLength = 1;

// how many times substitution should take place
int n = 6;

// time ticker
int time = 0;

// initial and final color values, for "color blending"
float r0 = 150, g0 = 100, b0 = 100;
float r1 = 200, g1 = 50, b1 = 50;
float r,g,b;

void setup() {
  
  size(800, 800);
  background(200,150,150);
  strokeWeight(1);
  
  // initialize and position turtle
  t = new Turtle(this);
  t.setX(500);
  t.setY(500);
  
  // perform the specified number of substitutions
  for (int i = 0; i < n; i++) {
    instructions = substitute(instructions, alphabet, substitutions);
  }
  instrLength = instructions.length();
  
}

void draw() {
  
  // optional delay, if you want to see the turtle move
  delay(1);
  
  // get the current instruction
  char c = instructions.charAt(time);
  
  // do color blending
  float p = float(time)/instrLength;
  println(p);
  r = p * r1 + (1-p) * r0;
  g = p * g1 + (1-p) * g0;
  b = p * b1 + (1-p) * b0;
  stroke(r,g,b);
  
  // translate each character into a turtle movement
  switch(c) {
     case 'F': {
       t.forward(4);
       break;
     }
     case '+': {
       t.left(90);
       break;
     }
     case '-': {
       t.right(90);
       break;
     }
  }
  
  // increment time, and stop if all instructions have been executed
  time += 1;
  if (time == instrLength) noLoop();
  
}

// given a string and an alphabet + substitution list defining substitution rules,
// return the string formed by performing those substitutions
String substitute(String str, char[] alph, String[] subs) {
  String newStr = "";
  int possibleChars = alph.length;
  for (int j = 0; j < str.length(); j++) {
    char c = str.charAt(j);
    for (int i = 0; i < possibleChars; i++) {
      char a = alph[i];
      if (c == a) {
        newStr += subs[i]; 
      }
    }
  }
  return newStr;
}
