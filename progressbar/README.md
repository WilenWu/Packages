创建可迭代的进度条类，执行任务的同时打印进度条。

## 包装迭代对象

使用`ProgressBar(iterable)`包装任何可迭代对象

```python
import time 
import progressbar as pbar

for char in pbar.ProgressBar('abcd'):
    time.sleep(0.05)
```

或者手动调用 `update` 方法更新

```python
import time 
import progressbar as pbar

x = range(100)
progress = pbar.ProgressBar(x, circle=True)
for i, value in enumerate(x):
    progress.update(i)
    time.sleep(0.05)
```

## 多任务进度条

创建多进度条实例，多线程调用任务

```python
import time 
import progressbar as pbar

# 处理迭代任务中的函数
def test_func(num,sec):
    time.sleep(sec)
    return num * 2

if __name__ == '__main__':
    bars = pbar.MultiProgressBar()
    bars.add_task('task1', pbar.ProgressBar(range(3),desc='task1'), test_func, 1)
    bars.add_task('task2', pbar.ProgressBar('ab',desc='task2'), test_func, 1)
    bars.add_task('task3', pbar.ProgressBar('ABCD',desc='task3'), test_func, 1)
    bars.start(['task2','task1', 'task3'])
```
