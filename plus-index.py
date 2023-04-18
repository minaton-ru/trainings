def find_sum(n, m):
    num_str = [str(i) for i in range(1, n+1)]
    results = [] # список для всех верных вариантов расстановки знака +
    def find_path_recur(start, path): # функция для рекурсивного поиска вариантов расстановки знаков
        if start == len(num_str): # если дошли до конца строки
            if eval(path) == m: # если результат выполнения path как выражения равен m, то добавляем вариант в список с результатами
                results.append(path)
            return
        find_path_recur(start+1, path+num_str[start]) # пропускаем текущую цифру
        find_path_recur(start+1, path+'+'+num_str[start]) # вставляем знак + перед последней цифрой
    find_path_recur(1, num_str[0]) # запускаем поиск вариантов с первой цифры и без знаков
    return results # возвращаем список всех вариантов

N, M = map(int, input().split())

res = find_sum(N, M)
for r in res:
    print(f'{r}={M}')
