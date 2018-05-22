# Sous
Sous operates along side Chef and Python much the same a sous-chef would
the executive chef and the rest of the kitchen. In order words, Sous 
implements the overall principles of Chef while managing the details.

### Chef vs Sous
Chef was an esoteric programming language developed by David Morgan-Mar.
The goal of the language was to produce programs that not only look like
cooking recipes, but also are cooking recipes. While it is possible to
write simple programs in Chef, the language lacks a number of features
taken for granted in today's languages. As such, Sous was created to 
allow for more complex programs while still holding true to Chef's
principles.

## Design Principles
1. Recipes should be edible and servings sizes proper. 
    - No need to waste food.
    
2. Ingredients must be real.
    - And edible.

3. Like Chef, measurements are metric.
    - Plus cups, tablespooons, and teaspoons.

## Syntax
Sous is built upon the base Chef syntax with some changes and additions.

### Recipe Title
> 1. Recipes titles must be present before all non-comment operations.
> 2. Titles must also describe the recipe and should be short. 
> 3. It is best practice to include a direct refrence to the operations of the program
>       - However, it is not  a necessity.

```
Recipe Title.
```

#### Example

```
Honey Butter.
```

### Prep (Function Definition)
> Indicates a function definition when followed by a period.
```
<Name Of Function> Prep.
<instructions>
```
#### Example
```
Egg Drop Soup Prep.
<instructions>
```

## Prep (Function Call)
> Indicates a function call when followed by a *title case* name and a period.
```
Prep <Name Of Function>.
```
#### Example
```
Prep Egg Drop Soup.
```

### Ingredients
