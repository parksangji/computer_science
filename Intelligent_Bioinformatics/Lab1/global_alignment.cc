#include<iostream>
#include<fstream>
#include<cstring>
#include<string>

using namespace std;

int Score_Matrix[100][100];

int match_score;
int mismatch_score;
int penalty;

void Global_Align(const string V,const  string W);

string Alignment_A;
string Alignment_B;

int main(void)
{
/*------------------------------------------------------------------------*/
    ifstream readfile("input.txt");

    int* first_line = new int[3];
    string V ;
    string W ;

    for(int j=0; j<3 ; j++) readfile >> first_line[j];

    getline(readfile,V);
    getline(readfile,V);
    getline(readfile,W);

    readfile.close();
 /*-------------------------------------------------------------------파일입력코드*/       
    match_score = first_line[0];
    mismatch_score = first_line[1];
    penalty = first_line[2];
/*-------------------------------------------------------------------------첫번째 줄 정수 값을 입력*/
    delete[] first_line;


    Global_Align(V,W);
    
    V.clear();
    W.clear();

}

void Global_Align(const string V,const string W)
{
    Score_Matrix[0][0] = 0;

    int V_size = V.size();
    int W_size = W.size();

    for(int i =0 ; i< V_size + 1; i++)
    {
        Score_Matrix[i][0] = penalty * i;
    }
    for(int j=0; j<W_size + 1 ; j++)
    {
        Score_Matrix[0][j] = penalty * j;
    }

    for(int i = 1; i < V_size +1; i++)
    {
        for(int j=1; j < W_size +1; j++)
        {
            int score_flag = 0;

            if(V[i-1] == W[j-1]) 
            {
                score_flag = Score_Matrix[i-1][j-1] + match_score;
            }

            else
            {
                score_flag = Score_Matrix[i-1][j-1] + mismatch_score;
            }

            int deletion = Score_Matrix[i-1][j] + penalty;
            int insertion = Score_Matrix[i][j-1] + penalty;
            Score_Matrix[i][j] = max(score_flag,max(deletion,insertion));   
        }
    }
    
/*------------------------------------------------------------------------traceBack*/
    Alignment_A = "";
    Alignment_B = "";
    int x = V.size();
    int y = W.size();

    while(x > 0 and y > 0)
    {
        int score_flag = 0;

        if(V[x-1] == W[y-1])
        {
            score_flag = match_score;
        }
        else
        {
            score_flag = mismatch_score;
        }
        
        if(x > 0 and y > 0 and Score_Matrix[x][y] == Score_Matrix[x-1][y-1] + score_flag)
        {
            Alignment_A = V[x-1] + Alignment_A;
            Alignment_B = W[y-1] + Alignment_B;
            x = x-1;
            y = y-1;
        }
        else if ( x > 0 and Score_Matrix[x][y] == Score_Matrix[x-1][y] + penalty)
        {
            Alignment_A = V[x-1] + Alignment_A;
            Alignment_B = "-" + Alignment_B;
            x = x -1;
        }
        else if ( y > 0 and Score_Matrix[x][y] == Score_Matrix[x][y-1] + penalty)
        {
            Alignment_A = "-" + Alignment_A;
            Alignment_B = W[y-1] + Alignment_B;
            y = y - 1;
        } 
    }
    int last_index = 0;
    int first_index = 0;

    for(int i=0; i< Alignment_A.size()+1; i++)
    {
        if(Alignment_A[i] == '-' or Alignment_B[i] == '-')
        {
            first_index = i;
            break;
        }
    }

    for(int i=0; i< Alignment_A.size()+1; i++)
    {
        if(Alignment_A[i] == '-' or Alignment_B[i] == '-')
        {
            last_index = i;
        }
    }
    int best_score = 0;

    for(int i =first_index-1; i< last_index +1 ; i++)
    {
        if(Alignment_A[i] == Alignment_B[i])
        {
            best_score += match_score;
        }
        else if(Alignment_B[i] == '-' or Alignment_A[i]== '-')
        {
            best_score += penalty;
        }
        else
        {
            best_score += mismatch_score;
        }   
    }
    if(last_index - first_index > 5) cout << best_score<< endl;
    else{cout << Score_Matrix[V.size()][W.size()] << endl;}
    
    cout << Alignment_A << endl;
    cout << Alignment_B << endl;

}