#pragma once
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

int countMount(int n, int& arr[][], int dir);
int step_available(int n, int& arr[][], int dir);
void createMap(int n, int& arr[][], int dir);
int return_direct(float& mounts[], float& steps[], float& base[]);