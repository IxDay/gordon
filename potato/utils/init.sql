SET client_min_messages TO WARNING;
SET search_path TO gordon,public;


-- insert a few number of ingredients
INSERT INTO ingredient (name) VALUES ('ingredient_1');
INSERT INTO ingredient (name) VALUES ('ingredient_2');
INSERT INTO ingredient (name) VALUES ('ingredient_3');
INSERT INTO ingredient (name) VALUES ('ingredient_4');
INSERT INTO ingredient (name) VALUES ('ingredient_5');
INSERT INTO ingredient (name) VALUES ('ingredient_6');
INSERT INTO ingredient (name) VALUES ('ingredient_7');
INSERT INTO ingredient (name) VALUES ('ingredient_8');
INSERT INTO ingredient (name) VALUES ('ingredient_9');


-- insert a few number of utensils
INSERT INTO utensil (name) VALUES ('utensil_1');
INSERT INTO utensil (name) VALUES ('utensil_2');
INSERT INTO utensil (name) VALUES ('utensil_3');
INSERT INTO utensil (name) VALUES ('utensil_4');
INSERT INTO utensil (name) VALUES ('utensil_5');
INSERT INTO utensil (name) VALUES ('utensil_6');
INSERT INTO utensil (name) VALUES ('utensil_7');
INSERT INTO utensil (name) VALUES ('utensil_8');
INSERT INTO utensil (name) VALUES ('utensil_9');


-- insert a few number of recipes
INSERT INTO
recipe (name, description, directions, difficulty, duration, people, category)
VALUES
(
    'recipe_1',
    'description recipe 1',
    '{
        "(step_1, instructions recipe 1 step 1)",
        "(step_2, instructions recipe 1 step 2)",
        "(step_3, instructions recipe 1 step 3)",
        "(step_4, instructions recipe 1 step 4)"
    }',
    1,
    '0/5',
    1,
    'starter'
);

INSERT INTO
recipe (name, description, directions, difficulty, duration, people, category)
VALUES
(
    'recipe_2',
    'description recipe 2',
    '{
        "(step_1, instructions recipe 2 step 1)",
        "(step_2, instructions recipe 2 step 2)",
        "(step_3, instructions recipe 2 step 3)",
        "(step_4, instructions recipe 2 step 4)"
    }',
    2,
    '5/10',
    2,
    'main'
);

INSERT INTO
recipe (name, directions, difficulty, duration, people, category)
VALUES
(
    'recipe_3',
    '{
        "(step_1, instructions recipe 3 step 1)",
        "(step_2, instructions recipe 3 step 2)",
        "(step_3, instructions recipe 3 step 3)",
        "(step_4, instructions recipe 3 step 4)"
    }',
    3,
    '10/15',
    3,
    'dessert'
);


-- recipe 1: ingredients
INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '1', 'L'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_1' AND ingredient.name = 'ingredient_1';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '2', 'g'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_1' AND ingredient.name = 'ingredient_4';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '3', 'oz'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_1' AND ingredient.name = 'ingredient_7';


-- recipe 2: ingredients
INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '4', 'spoon'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_2' AND ingredient.name = 'ingredient_2';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '5', 'L'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_2' AND ingredient.name = 'ingredient_5';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '6', 'g'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_2' AND ingredient.name = 'ingredient_8';


-- recipe 3: ingredients
INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '7', 'oz'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_3' AND ingredient.name = 'ingredient_3';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '8', 'spoon'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_3' AND ingredient.name = 'ingredient_6';

INSERT INTO recipe_ingredients
    (fk_recipe, fk_ingredient, quantity, measurement)
SELECT recipe.id, ingredient.id, '9', 'L'
FROM recipe AS recipe, ingredient AS ingredient
WHERE recipe.name = 'recipe_3' AND ingredient.name = 'ingredient_9';


-- recipe 1: utensils
INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_1' AND utensil.name = 'utensil_1';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_1' AND utensil.name = 'utensil_4';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_1' AND utensil.name = 'utensil_7';


-- recipe 2: utensils
INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_2' AND utensil.name = 'utensil_2';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_2' AND utensil.name = 'utensil_5';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_2' AND utensil.name = 'utensil_8';


-- recipe 3: utensils
INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_3' AND utensil.name = 'utensil_3';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_3' AND utensil.name = 'utensil_6';

INSERT INTO recipe_utensils
    (fk_recipe, fk_utensil)
SELECT recipe.id, utensil.id
FROM recipe AS recipe, utensil AS utensil
WHERE recipe.name = 'recipe_3' AND utensil.name = 'utensil_9';

