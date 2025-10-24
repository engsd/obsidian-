# 专升本数学第一章：函数、极限与连续 - 标准操作流程 (SOP)

## 1.0 模块概述: `functions_and_limits.py`

### 1.1 模块功能简介

本模块是 `ZSB_Math` 代码库中的核心模块，专门处理专升本数学第一章"函数、极限与连续"的所有问题类型。该模块采用面向对象的设计模式，将复杂的数学问题分解为三个独立且协作的类，每个类负责特定的功能领域。

**核心设计理念：**
- **模块化分离**：将函数属性分析、极限求解、连续性检验分离为独立模块
- **原子化工具**：每个解题方法都是独立的、可复用的原子化工具
- **策略与工具分层**：高层决策类调用底层工具函数，实现关注点分离

### 1.2 依赖项 (Dependencies)

```python
import algebra_toolkit  # 基础代数工具箱
import numpy as np      # 数值计算支持
import sympy as sp      # 符号计算支持
```

---

## 2.0 类定义: `Function_Properties` (函数属性分析器)

### 2.1 功能描述

`Function_Properties` 类负责分析函数的基本属性，包括定义域、值域、奇偶性、单调性、周期性等。这是解决函数相关问题的基础工具类。

### 2.2 方法清单 (Method Catalog)

#### 2.2.1 `get_domain()`: 求解定义域

**功能描述 (Description):**
确定函数的定义域，即函数有意义的自变量取值范围。

**触发条件 (Triggers):**
- 遇到分母含有变量的分式函数
- 遇到根式函数（偶次根式）
- 遇到对数函数
- 遇到反三角函数
- 遇到复合函数

**执行步骤 (Procedure):**
```python
def get_domain(self, function_expr):
    # Step 1: 识别函数类型
    function_type = self._identify_function_type(function_expr)
    
    # Step 2: 根据函数类型应用相应规则
    if "fraction" in function_type:
        # 分母不为零
        constraints = self._solve_denominator_nonzero(function_expr)
    elif "sqrt" in function_type:
        # 偶次根式被开方数非负
        constraints = self._solve_radicand_nonnegative(function_expr)
    elif "log" in function_type:
        # 真数大于零
        constraints = self._solve_argument_positive(function_expr)
    
    # Step 3: 求交集得到最终定义域
    domain = self._intersect_constraints(constraints)
    return domain
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 复合函数的定义域需要同时满足内外函数的定义域要求
- 分段函数需要分别考虑各段的定义域
- 隐函数的定义域求解需要特别小心

#### 2.2.2 `check_parity()`: 判断奇偶性

**功能描述 (Description):**
判断函数是奇函数、偶函数还是非奇非偶函数。

**触发条件 (Triggers):**
- 题目要求判断函数的奇偶性
- 需要利用函数奇偶性简化计算
- 积分计算中需要利用奇偶性质

**执行步骤 (Procedure):**
```python
def check_parity(self, function_expr):
    # Step 1: 检查定义域是否关于原点对称
    domain = self.get_domain(function_expr)
    if not self._is_symmetric_about_origin(domain):
        return "非奇非偶函数（定义域不对称）"
    
    # Step 2: 计算 f(-x)
    f_minus_x = function_expr.subs(x, -x)
    
    # Step 3: 比较 f(-x) 与 f(x) 和 -f(x)
    if f_minus_x.equals(function_expr):
        return "偶函数"
    elif f_minus_x.equals(-function_expr):
        return "奇函数"
    else:
        return "非奇非偶函数"
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 必须先检查定义域是否关于原点对称
- 注意三角函数的奇偶性判断
- 复合函数的奇偶性判断需要特别小心

#### 2.2.3 `analyze_monotonicity()`: 单调性分析

**功能描述 (Description):**
分析函数在给定区间上的单调性。

**触发条件 (Triggers):**
- 需要求函数的单调区间
- 比较函数值大小
- 求函数的最值

**执行步骤 (Procedure):**
```python
def analyze_monotonicity(self, function_expr, interval=None):
    # Step 1: 求导数
    derivative = sp.diff(function_expr, x)
    
    # Step 2: 求导数的零点和不存在点
    critical_points = sp.solve(derivative, x)
    undefined_points = self._find_undefined_points(derivative)
    
    # Step 3: 划分区间并判断导数符号
    test_intervals = self._create_test_intervals(critical_points, undefined_points)
    monotonicity_info = []
    
    for interval in test_intervals:
        test_point = self._choose_test_point(interval)
        derivative_value = derivative.subs(x, test_point)
        
        if derivative_value > 0:
            monotonicity_info.append((interval, "递增"))
        elif derivative_value < 0:
            monotonicity_info.append((interval, "递减"))
    
    return monotonicity_info
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 注意导数不存在的点
- 驻点不一定是极值点
- 需要考虑函数的定义域

---

## 3.0 类定义: `Limit_Solver` (极限求解器)

### 3.1 功能描述

`Limit_Solver` 类是本模块的核心决策类，负责求解各种类型的极限问题。该类实现了一套完整的极限求解决策算法，能够自动选择最适合的方法来解决极限问题。

### 3.2 核心决策算法: `solve()` 方法

**极限求解决策树：**

```mermaid
graph TD
    A[输入极限问题] --> B[直接代入检查]
    B --> C{是否为确定形式?}
    C -->|是| D[返回极限值]
    C -->|否| E{未定式类型判断}
    
    E --> F[0/0型]
    E --> G[∞/∞型]
    E --> H[0·∞型]
    E --> I[∞-∞型]
    E --> J[1^∞型]
    E --> K[0^0型]
    E --> L[∞^0型]
    
    F --> M[代数变形策略]
    M --> N{是否成功?}
    N -->|否| O[洛必达法则]
    N -->|是| D
    
    G --> O
    O --> P{是否成功?}
    P -->|否| Q[等价无穷小替换]
    P -->|是| D
    
    H --> R[转化为0/0或∞/∞]
    I --> S[通分或有理化]
    J --> T[指数型处理: e^(ln)]
    K --> T
    L --> T
    
    Q --> U{是否成功?}
    U -->|否| V[两个重要极限]
    U -->|是| D
    
    V --> W{是否成功?}
    W -->|否| X[泰勒展开]
    W -->|是| D
    
    X --> D
```

### 3.3 方法清单 (Atomic Tools Catalog)

#### 3.3.1 `_check_form_by_direct_substitution()`: 直接代入检查法

**功能描述 (Description):**
通过直接代入自变量的趋向值来检查极限是否为确定形式。

**触发条件 (Triggers):**
- 所有极限问题的第一步
- 函数在趋向点连续时

**执行步骤 (Procedure):**
```python
def _check_form_by_direct_substitution(self, expr, var, limit_point):
    # Step 1: 直接代入
    try:
        result = expr.subs(var, limit_point)
        
        # Step 2: 判断结果类型
        if result.is_finite and result.is_real:
            return {"type": "确定形式", "value": result}
        elif result.is_infinite:
            return {"type": "无穷大", "value": result}
        else:
            return {"type": "未定式", "form": self._identify_indeterminate_form(result)}
    except:
        return {"type": "未定式", "form": "需要进一步分析"}
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 注意区分 +∞ 和 -∞
- 0/0 和 ∞/∞ 是最常见的未定式
- 有些函数在某点不连续但极限存在

#### 3.3.2 `_apply_lhopitals_rule()`: 洛必达法则

**功能描述 (Description):**
对 0/0 型和 ∞/∞ 型未定式应用洛必达法则。

**触发条件 (Triggers):**
- 直接代入得到 0/0 型未定式
- 直接代入得到 ∞/∞ 型未定式
- 代数变形无法简化时

**执行步骤 (Procedure):**
```python
def _apply_lhopitals_rule(self, numerator, denominator, var, limit_point):
    # Step 1: 验证洛必达法则的适用条件
    if not self._verify_lhopital_conditions(numerator, denominator, var, limit_point):
        return None
    
    # Step 2: 分别对分子分母求导
    num_derivative = sp.diff(numerator, var)
    den_derivative = sp.diff(denominator, var)
    
    # Step 3: 构造新的极限表达式
    new_expr = num_derivative / den_derivative
    
    # Step 4: 递归求解新极限
    return self.solve(new_expr, var, limit_point)
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 必须验证分子分母都趋向于0或∞
- 导数的极限必须存在
- 可能需要多次应用洛必达法则
- 有时洛必达法则会使问题复杂化

#### 3.3.3 `_use_equivalent_infinitesimals()`: 等价无穷小替换

**功能描述 (Description):**
利用等价无穷小关系简化极限计算。

**触发条件 (Triggers):**
- x → 0 时出现 sin(x), tan(x), ln(1+x), e^x-1, (1+x)^α-1 等
- 分子或分母包含常见的等价无穷小

**执行步骤 (Procedure):**
```python
def _use_equivalent_infinitesimals(self, expr, var, limit_point):
    # Step 1: 识别可替换的等价无穷小
    equivalent_pairs = {
        'sin(x)': 'x',
        'tan(x)': 'x', 
        'ln(1+x)': 'x',
        'exp(x)-1': 'x',
        '1-cos(x)': 'x**2/2',
        'arcsin(x)': 'x',
        'arctan(x)': 'x'
    }
    
    # Step 2: 执行替换（仅在乘除法中）
    simplified_expr = expr
    for original, equivalent in equivalent_pairs.items():
        if self._can_replace_safely(expr, original):
            simplified_expr = simplified_expr.subs(original, equivalent)
    
    # Step 3: 计算简化后的极限
    return self._check_form_by_direct_substitution(simplified_expr, var, limit_point)
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 等价无穷小只能在乘除法中使用，不能在加减法中直接使用
- 必须确保替换后的表达式仍然趋向于同一点
- 复合函数的等价无穷小需要特别小心

#### 3.3.4 `_handle_indeterminate_powers()`: 指数型未定式处理

**功能描述 (Description):**
处理 1^∞, 0^0, ∞^0 型未定式。

**触发条件 (Triggers):**
- 底数趋向于1，指数趋向于∞
- 底数趋向于0，指数趋向于0
- 底数趋向于∞，指数趋向于0

**执行步骤 (Procedure):**
```python
def _handle_indeterminate_powers(self, base, exponent, var, limit_point):
    # Step 1: 取对数转化
    # lim f(x)^g(x) = exp(lim g(x) * ln(f(x)))
    
    log_expr = exponent * sp.ln(base)
    
    # Step 2: 求解指数部分的极限
    exponent_limit = self.solve(log_expr, var, limit_point)
    
    # Step 3: 计算最终结果
    if exponent_limit.is_finite:
        return sp.exp(exponent_limit)
    elif exponent_limit == sp.oo:
        return sp.oo
    elif exponent_limit == -sp.oo:
        return 0
    else:
        return None
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 必须确保底数大于0（对数有意义）
- 转化后可能得到 0·∞ 型未定式
- 需要特别注意符号问题

#### 3.3.5 `_use_two_important_limits()`: 两个重要极限

**功能描述 (Description):**
应用两个重要极限：lim(x→0) sin(x)/x = 1 和 lim(x→∞) (1+1/x)^x = e。

**触发条件 (Triggers):**
- 出现 sin(x)/x 或类似形式
- 出现 (1+1/x)^x 或 (1+x)^(1/x) 形式
- 可以通过变量替换转化为重要极限形式

**执行步骤 (Procedure):**
```python
def _use_two_important_limits(self, expr, var, limit_point):
    # Step 1: 识别重要极限模式
    if self._matches_first_important_limit(expr, var, limit_point):
        # lim(t→0) sin(t)/t = 1 的变形
        return self._apply_first_important_limit(expr, var, limit_point)
    
    elif self._matches_second_important_limit(expr, var, limit_point):
        # lim(t→∞) (1+1/t)^t = e 的变形
        return self._apply_second_important_limit(expr, var, limit_point)
    
    else:
        return None
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 需要通过适当的变量替换转化为标准形式
- 注意系数的处理
- 复合函数情况下的应用

#### 3.3.6 `_use_algebraic_manipulation()`: 代数变形策略

**功能描述 (Description):**
通过代数变形（因式分解、有理化、通分等）简化极限表达式。

**触发条件 (Triggers):**
- 0/0 型未定式且可以约去公因子
- 含有根式的表达式
- 分式的分子分母有公因子

**执行步骤 (Procedure):**
```python
def _use_algebraic_manipulation(self, expr, var, limit_point):
    # Step 1: 尝试因式分解
    factored = algebra_toolkit.factor_polynomial(expr)
    if factored != expr:
        return self.solve(factored, var, limit_point)
    
    # Step 2: 尝试有理化
    rationalized = algebra_toolkit.rationalize_expression(expr)
    if rationalized != expr:
        return self.solve(rationalized, var, limit_point)
    
    # Step 3: 尝试三角恒等变形
    trig_simplified = algebra_toolkit.trig_identity_transform(expr)
    if trig_simplified != expr:
        return self.solve(trig_simplified, var, limit_point)
    
    return None
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 变形必须在定义域内等价
- 有理化时注意符号
- 因式分解可能引入新的零点

---

## 4.0 类定义: `Continuity_Checker` (连续性检验器)

### 4.1 功能描述

`Continuity_Checker` 类负责判断函数的连续性，包括连续点的判断、间断点的分类等。

### 4.2 方法清单 (Method Catalog)

#### 4.2.1 `is_continuous()`: 判断连续性

**功能描述 (Description):**
判断函数在指定点或区间上的连续性。

**触发条件 (Triggers):**
- 需要判断函数在某点是否连续
- 分析函数的连续区间
- 求函数的间断点

**执行步骤 (Procedure):**
```python
def is_continuous(self, function_expr, point):
    # Step 1: 检查函数在该点是否有定义
    try:
        function_value = function_expr.subs(x, point)
        if not function_value.is_finite:
            return False, "函数在该点无定义"
    except:
        return False, "函数在该点无定义"
    
    # Step 2: 计算左右极限
    left_limit = self.limit_solver.solve(function_expr, x, point, direction='-')
    right_limit = self.limit_solver.solve(function_expr, x, point, direction='+')
    
    # Step 3: 检查连续性的三个条件
    if left_limit != right_limit:
        return False, "左右极限不相等"
    elif left_limit != function_value:
        return False, "极限值与函数值不相等"
    else:
        return True, "函数在该点连续"
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 必须同时检查三个条件：函数有定义、极限存在、极限值等于函数值
- 注意左右极限的计算
- 分段函数在分界点的连续性需要特别注意

#### 4.2.2 `classify_discontinuity()`: 判断间断点类型

**功能描述 (Description):**
对间断点进行分类：可去间断点、跳跃间断点、无穷间断点、振荡间断点。

**触发条件 (Triggers):**
- 确定函数在某点不连续后
- 需要分析间断点的性质

**执行步骤 (Procedure):**
```python
def classify_discontinuity(self, function_expr, point):
    # Step 1: 计算左右极限
    left_limit = self.limit_solver.solve(function_expr, x, point, direction='-')
    right_limit = self.limit_solver.solve(function_expr, x, point, direction='+')
    
    # Step 2: 根据左右极限的情况分类
    if left_limit == right_limit and left_limit.is_finite:
        return "可去间断点", f"极限值为 {left_limit}"
    
    elif left_limit.is_finite and right_limit.is_finite and left_limit != right_limit:
        return "跳跃间断点", f"左极限 {left_limit}, 右极限 {right_limit}"
    
    elif left_limit.is_infinite or right_limit.is_infinite:
        return "无穷间断点", f"左极限 {left_limit}, 右极限 {right_limit}"
    
    else:
        return "振荡间断点", "极限不存在且不为无穷"
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 可去间断点可以通过重新定义函数值来"去除"
- 跳跃间断点的左右极限都存在但不相等
- 无穷间断点至少有一侧极限为无穷
- 振荡间断点的极限不存在（如 sin(1/x) 在 x=0 处）

---

## 5.0 附录A: 基础工具箱 `algebra_toolkit.py`

### 5.1 功能描述

`algebra_toolkit.py` 是底层工具模块，提供各种基础的代数运算功能，被上层类的方法调用。该模块实现了关注点分离的设计原则，将纯计算功能与决策逻辑分离。

### 5.2 函数清单 (Utility Function Catalog)

#### 5.2.1 `factor_polynomial()`: 多项式因式分解

**功能描述 (Description):**
对多项式进行因式分解，包括提取公因子、十字相乘法、完全平方公式等。

**触发条件 (Triggers):**
- 分子分母有公因子需要约简
- 0/0 型极限需要约去零因子
- 求解方程需要因式分解

**执行步骤 (Procedure):**
```python
def factor_polynomial(expr):
    # Step 1: 尝试提取公因子
    factored = sp.factor(expr)
    
    # Step 2: 如果标准因式分解失败，尝试特殊方法
    if factored == expr:
        # 尝试配方法
        completed_square = _try_complete_square(expr)
        if completed_square != expr:
            return completed_square
        
        # 尝试分组分解
        grouped = _try_grouping(expr)
        if grouped != expr:
            return grouped
    
    return factored
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 有些多项式在实数范围内不能分解
- 注意分解后的符号
- 复杂表达式可能需要多步分解

#### 5.2.2 `rationalize_expression()`: 表达式有理化

**功能描述 (Description):**
对含有根式的表达式进行有理化处理。

**触发条件 (Triggers):**
- 分母含有根式
- ∞-∞ 型未定式需要通分
- 需要化简根式表达式

**执行步骤 (Procedure):**
```python
def rationalize_expression(expr):
    # Step 1: 识别需要有理化的部分
    if _has_sqrt_in_denominator(expr):
        return _rationalize_denominator(expr)
    
    elif _is_difference_of_sqrts(expr):
        return _rationalize_numerator(expr)
    
    else:
        return expr

def _rationalize_denominator(expr):
    # 分母有理化：乘以共轭表达式
    numerator, denominator = sp.fraction(expr)
    conjugate = _get_conjugate(denominator)
    
    new_numerator = sp.expand(numerator * conjugate)
    new_denominator = sp.expand(denominator * conjugate)
    
    return new_numerator / new_denominator
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 有理化后表达式可能变得更复杂
- 注意根式的定义域
- 多重根式的有理化需要多步进行

#### 5.2.3 `trig_identity_transform()`: 三角函数恒等变形

**功能描述 (Description):**
利用三角恒等式对三角函数表达式进行变形。

**触发条件 (Triggers):**
- 含有三角函数的极限问题
- 需要化简三角表达式
- 利用三角函数的周期性和对称性

**执行步骤 (Procedure):**
```python
def trig_identity_transform(expr):
    # Step 1: 应用基本恒等式
    # sin²x + cos²x = 1
    expr = expr.subs(sp.sin(x)**2 + sp.cos(x)**2, 1)
    
    # Step 2: 应用二倍角公式
    expr = _apply_double_angle_formulas(expr)
    
    # Step 3: 应用和差化积公式
    expr = _apply_sum_to_product_formulas(expr)
    
    # Step 4: 应用积化和差公式
    expr = _apply_product_to_sum_formulas(expr)
    
    return sp.simplify(expr)
```

**注意事项/陷阱 (Cautions/Pitfalls):**
- 三角变形可能有多种方向，需要选择合适的
- 注意三角函数的定义域和值域
- 某些恒等变形可能引入额外的周期

---

## 总结

本SOP文档提供了一套完整的、系统化的专升本数学第一章问题解决方案。通过模块化设计和原子化工具的组合，能够有效处理函数、极限与连续性相关的各类问题。

**使用建议：**
1. 遇到问题时，首先确定问题类型，选择对应的类
2. 按照决策树的流程，系统地尝试各种方法
3. 注意各方法的适用条件和注意事项
4. 善用基础工具箱中的辅助函数

**扩展方向：**
- 可以根据实际需要添加更多的原子化工具
- 可以优化决策算法，提高求解效率
- 可以添加可视化功能，帮助理解解题过程