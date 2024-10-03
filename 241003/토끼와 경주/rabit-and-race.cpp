#include <vector>
#include <iostream>
#include <algorithm>
#include <unordered_map>
#include <queue>
using namespace std;

struct Rabbit
{
    int pid;
    long long d;
    int x;
    int y;
    int jump;

    Rabbit(int pid_, long long d_) : pid(pid_), d(d_), x(1), y(1), jump(0) {}
};

struct HeapEntry
{
    int jump;
    int sum_xy;
    int x;
    int y;
    int pid;
};

struct CompareHeapEntry
{
    bool operator()(const HeapEntry &a, const HeapEntry &b) const
    {
        if (a.jump != b.jump)
            return a.jump > b.jump;
        if (a.sum_xy != b.sum_xy)
            return a.sum_xy > b.sum_xy;
        if (a.x != b.x)
            return a.x > b.x;
        if (a.y != b.y)
            return a.y > b.y;
        return a.pid > b.pid;
    }
};

pair<int, int> calc(int x, int y, long long d, int dx, int dy, int N, int M)
{
    int nx, ny;

    if (dx != 0)
    {
        int period = 2 * (N - 1);
        long long tmp = (x - 1) + (long long)dx * d;
        tmp %= period;
        if (tmp < 0)
            tmp += period;
        tmp = min((long long)tmp, (long long)(period - tmp));
        nx = tmp + 1;
    }
    else
    {
        nx = x;
    }

    if (dy != 0)
    {
        int period = 2 * (M - 1);
        long long temp = (y - 1) + (long long)dy * d;
        temp %= period;
        if (temp < 0)
            temp += period;
        temp = min((long long)temp, (long long)(period - temp));
        ny = temp + 1;
    }
    else
    {
        ny = y;
    }

    return {nx, ny};
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int Q;
    cin >> Q;

    unordered_map<int, Rabbit> rabbits;

    priority_queue<HeapEntry, vector<HeapEntry>, CompareHeapEntry> heap;

    unordered_map<int, long long> scores;

    int N = 0, M = 0;

    while (Q--)
    {
        int q;
        cin >> q;

        if (q == 100)
        {
            int P;
            cin >> N >> M >> P;
            for (int j = 0; j < P; ++j)
            {
                int pid;
                long long d;
                cin >> pid >> d;
                Rabbit rabbit(pid, d);
                rabbits.emplace(pid, rabbit);

                HeapEntry he;
                he.jump = rabbit.jump;
                he.sum_xy = rabbit.x + rabbit.y;
                he.x = rabbit.x;
                he.y = rabbit.y;
                he.pid = rabbit.pid;
                heap.push(he);
            }
        }
        else if (q == 200)
        {
            int K;
            long long S;
            cin >> K >> S;
            vector<tuple<long long, long long, long long, long long, int>> r_best;

            for (int j = 0; j < K; ++j)
            {
                if (heap.empty())
                    break;
                HeapEntry he = heap.top();
                heap.pop();
                int pid = he.pid;

                auto it = rabbits.find(pid);
                if (it == rabbits.end())
                    continue;
                Rabbit &rabbit = it->second;

                if (he.jump != rabbit.jump || he.sum_xy != (rabbit.x + rabbit.y) || he.x != rabbit.x || he.y != rabbit.y || he.pid != rabbit.pid)
                    continue;

                vector<pair<int, int>> directions = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
                vector<tuple<long long, long long, long long, long long, long long>> candi_vec;

                for (auto &[dx, dy] : directions)
                {
                    pair<int, int> new_pos = calc(rabbit.x, rabbit.y, rabbit.d, dx, dy, N, M);
                    int nx = new_pos.first;
                    int ny = new_pos.second;
                    candi_vec.emplace_back(-(long long)(nx + ny), -(long long)nx, -(long long)ny, (long long)nx, (long long)ny);
                }

                sort(candi_vec.begin(), candi_vec.end());

                auto chosen = candi_vec[0];
                long long nx = get<3>(chosen);
                long long ny = get<4>(chosen);

                rabbit.x = nx;
                rabbit.y = ny;
                rabbit.jump += 1;

                HeapEntry new_he;
                new_he.jump = rabbit.jump;
                new_he.sum_xy = rabbit.x + rabbit.y;
                new_he.x = rabbit.x;
                new_he.y = rabbit.y;
                new_he.pid = rabbit.pid;
                heap.push(new_he);

                long long score = nx + ny;
                for (auto &[o_pid, o_rabbit] : rabbits)
                {
                    if (o_pid != pid)
                    {
                        scores[o_pid] += score;
                    }
                }

                // Store this rabbit's data as a candidate for the best rabbit
                r_best.emplace_back(-(nx + ny), -nx, -ny, -(long long)pid, pid);
            }

            if (!r_best.empty())
            {
                sort(r_best.begin(), r_best.end());
                int best_pid = get<4>(r_best[0]);
                scores[best_pid] += S;
            }
        }
        else if (q == 300)
        {
            int pid_t;
            long long L;
            cin >> pid_t >> L;
            auto it = rabbits.find(pid_t);
            if (it != rabbits.end())
            {
                it->second.d *= L;
            }
        }
        else if (q == 400)
        {
            long long max_score = 0;
            for (auto &[pid, score] : scores)
            {
                if (score > max_score)
                    max_score = score;
            }
            cout << max_score << "\n";
        }
    }
}