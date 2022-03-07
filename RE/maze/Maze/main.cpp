#include <iostream>
#include<stdio.h>

#define INWALL 1
#define BLOODEMPTY 2
#define WIN 3
#define NORMAL 0
#define UNKNOWN 4
//#define DEBUG

typedef struct coord {
	int x;
	int y;
}coord;

enum place_type {
	N,
	W,
	B,			//血量增加
	D			//血量减少
};

typedef struct place {
	place_type pt;
	unsigned char degree;	
}*pplace;

class Map {
private:
	int size;
	pplace grid;
public:
	Map(int size) {
		this->size = size;
		grid = (place*)malloc(this->size * this->size * sizeof(place));
	}
	void SetMap(enum place_type* SetType, unsigned char* SetDegree) {
		for (int i = 0; i <= size * size; i++) {
			grid[i].pt = SetType[i];
			grid[i].degree = SetDegree[i];
		}
	}
	place_type GetPlaceType(coord c) {
		return grid[c.x + c.y * size].pt;
	}
	unsigned char GetPlaceDegree(coord c) {
		return grid[c.x + c.y * size].degree;
	}
	int GetSize() {
		return size;
	}
};

class Person {
private:
	int blood;
	coord c;
public:
	Person(coord sc, int blood) {
		c = sc;
		this->blood = blood;
	}
	void UpDateStatus(coord sc, Map mp) {
		c = sc;
		if (mp.GetPlaceType(c) == D) {
			blood -= mp.GetPlaceDegree(sc);
		}
		else if(mp.GetPlaceType(c) == B){
			blood += mp.GetPlaceDegree(sc);
		}

	}
	coord GetPlace() {
		return c;
	}
	int GetBlood() {
		return blood;
	}
	int CheckStatus(Map mp) {
		if(mp.GetPlaceType(c) == W){
			return INWALL;
		}
		if (blood < 1) {
			return BLOODEMPTY;
		}
		if (c.x == mp.GetSize() - 1 && c.y == mp.GetSize() - 1) {
			return WIN;
		}
		if (mp.GetPlaceType(c) == N || mp.GetPlaceType(c) == B || mp.GetPlaceType(c) == D) {
			return NORMAL;
		}
		return UNKNOWN;
	}
};



int main() {
	Map map = Map(10);
	place_type pt[100] = {
N, N, N, N, N, N, N, N, N, W,
W, N, W, W, N, W, W, N, W, W,
W, N, W, W, N, W, W, N, W, W,
W, N, W, W, N, W, W, N, W, W,
W, B, W, W, B, W, W, B, W, W,
W, N, W, W, N, W, W, N, W, W,
W, N, W, W, N, W, W, N, W, W,
W, D, W, W, D, W, W, D, W, W,
W, N, W, W, N, W, W, N, W, W,
W, D, N, N, D, N, N, D, N, N
	};
	unsigned char sd[100] = {
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 128, 0, 0, 135, 0, 0, 111, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 50, 0, 0, 94, 0, 0, 79, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 40, 0, 0, 8, 0, 0, 33, 0, 0
	};

	map.SetMap(pt,sd);
	coord sc;
	sc.x = 0;
	sc.y = 0;
	int blood = 1;

	Person p = Person(sc, blood);
	int count = 0;
	for (char c; (c = getchar(), c != '\n');count ++) {
#ifdef DEBUG
		std::cout << count << std::endl;
#endif // DEBUG
		switch(c){
			case 'w':
				sc = p.GetPlace();
				sc.y -= 1;
				p.UpDateStatus(sc,map);
				break;
			case 'a':
				sc = p.GetPlace();
				sc.x -= 1;
				p.UpDateStatus(sc, map);
				break;
			case 's':
				sc = p.GetPlace();
				sc.y += 1;
				p.UpDateStatus(sc, map);
				break;
			case 'd':
				sc = p.GetPlace();
				sc.x += 1;
				p.UpDateStatus(sc, map);
				break;
			default:
				std::cout << "Wrong Input!" << std::endl;
				return 0;
				continue;
		}
		if (count > 17) {
			std::cout << "Wrong Length!" << std::endl;
			return 0;
		}
		if (p.CheckStatus(map) == BLOODEMPTY) {
			std::cout << "You Die!" << std::endl;
			return 0;
#ifdef DEBUG
			std::cout << p.GetPlace().x << "," << p.GetPlace().y << "," << p.GetBlood() << std::endl;
#endif
		}
		else if (p.CheckStatus(map) == INWALL) {
			std::cout << "You Are In The Wall!" << std::endl;
			return 0;
#ifdef DEBUG
			std::cout << p.GetPlace().x << "," << p.GetPlace().y << "," << p.GetBlood() << std::endl;
#endif
		}
		else if (p.CheckStatus(map) == WIN) {
			std::cout << "You WIN! The flag is flag{YOUR INPUT}!" << std::endl;
			return 0;
#ifdef DEBUG
			std::cout << p.GetPlace().x << "," << p.GetPlace().y << "," << p.GetBlood() << std::endl;
#endif
		}
		else {
#ifdef DEBUG
			std::cout << p.GetPlace().x << "," << p.GetPlace().y << "," << p.GetBlood() << std::endl;
#endif
		}
	}
	return 0;
}
