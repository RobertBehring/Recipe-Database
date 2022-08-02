import json

# ingredient densities are all grams / cup
ingredient_densities = {
    "all-purpose flour": 120 / 1,
    "baking powder": 4 / 0.0208,
    "baking soda": 3 / 0.0104,
    "bread flour": 120 / 1,
    "brown sugar": 213 / 1,
    "butter": 113 / 0.5,
    "carrots": 142 / 1,  # diced
    "celery": 142 / 1,  # diced
    "feta cheese": 57 / 0.5,
    "cheddar cheese": 113 / 1,  # grated
    "cherries": 113 / 1,  # frozen,
    "chocolate chips": 170 / 1,
    "cocoa": 42 / 0.5,
    "coconut": 85 / 1,
    "corn syrup": 312 / 1,
    "cranberries": 99 / 1,
    "cream": 227 / 1,
    "cream cheese": 227 / 1,
    "creme fraiche": 124 / 0.5,
    "dates": 149 / 1,
    "dried milk": 28 / 0.25,
    "potato flakes": 43 / 0.5,
    "large egg": 50 / 0.25,
    "figs": 149 / 1,
    "flax meal": 50 / 0.5,
    "minced garlic": 28 / 0.125,
    "peeled garlic": 149 / 1,
    "ghee": 44 / 0.25,
    "gluten-free all-purpose flour": 156 / 1,
    "granola": 113 / 1,
    "hazelnuts": 142 / 1,
    "honey": 21 / 0.0625,
    "jam": 85 / 0.25,
    "preserves": 85 / 0.25,
    "lard": 113 / 0.5,
    "leeks": 92 / 1,
    "lemon juice": 14 / 0.0625,
    "macadamia nuts": 149 / 1,
    "maple syrup": 156 / 0.5,
    "marshmallow spread": 123 / 1,
    "mini marshmallows": 43 / 1,
    "marzipan": 290 / 1,
    "masa harina": 93 / 1,
    "mascarpone cheese": 227 / 1,
    "mayonnaise": 113 / 0.5,
    "evaporated milk": 113 / 0.5,
    "milk": 227 / 1,
    "molasses": 85 / 0.25,
    "mushrooms": 78 / 1,  # sliced
    "oat flour": 92 / 1,
    "old fashioned oats": 89 / 1,
    "olive oil": 50 / 0.25,
    "olives": 142 / 1,  # sliced
    "onions": 142 / 1,  # diced
    "paleo baking flour": 104 / 1,
    "palm shortening": 45 / 0.25,
    "pastry flour": 106 / 1,
    "peaches": 170 / 1,
    "peanut butter": 135 / 0.5,
    "peanuts": 142 / 1,
    "pears": 163 / 1,
    "pecans": 57 / 0.5,
    "pine nuts": 71 / 0.5,
    "pineapple": 170 / 1,
    "pistachio nuts": 60 / 0.5,
    "pizza sauce": 57 / 0.5,
    "poppy seeds": 18 / 0.125,
    "quinoa": 177 / 1,  # whole
    "raisins": 85 / 0.5,
    "raspberries": 120 / 1,
    "rhubarb": 120 / 1,
    "rice": 99 / 0.5,
    "table salt": 18 / 0.0625,
    "semolina flour": 163 / 1,
    "sesame seeds": 71 / 0.5,
    "sour cream": 227 / 1,
    "sourdough starter": 234 / 1,
    "steel cut oats": 70 / 0.5,
    "strawberries": 167 / 1,
    "white sugar": 198 / 1,
    "sweetened condensed milk": 78 / 0.25,
    "tahini": 128 / 0.5,
    "tapioca flour": 113 / 1,
    "tomato paste": 29 / 0.125,
    "turbinado sugar": 180 / 1,
    "vanilla extract": 14 / 0.0625,
    "vegetable oil": 198 / 1,
    "vegetable shortening": 46 / 0.25,
    "walnuts": 64 / 0.5,
    "water": 227 / 1,
    "instant yeast": 9 / 0.0625,
    "yogurt": 227 / 1,
    "zucchini": 136 / 1
}
metric_mass_unit_factors = {"mg": 1 / 0.001, "g": 1, "kg": 1 / 1000}
metric_mass_units = list(metric_mass_unit_factors.keys())
metric_volume_unit_factors = {"ml": 1 / 0.001, "l": 1, "kl": 1 / 1000}
metric_volume_units = list(metric_volume_unit_factors.keys())
metric_to_imperial_mass = 1 / 28.35
metric_to_imperial_vol = 1 / 0.236

imperial_mass_unit_factors = {"oz": 1, "lb": 1 / 16}
imperial_mass_units = list(imperial_mass_unit_factors.keys())
imperial_volume_unit_factors = {"gal": 1 / 16, "qt": 1 / 4, "pt": 1 / 2, "c": 1, "fl oz": 8, "tbsp": 16, "tsp": 48}
imperial_volume_units = list(imperial_volume_unit_factors.keys())
imperial_to_metric_mass = 28.35
imperial_to_metric_vol = 0.236


def conversion(data: dict):
    if type(data) == str:
        data = json.loads(data)
    recipe_list = list(data.keys())
    converted = None

    for recipe_name in recipe_list:
        converted = {recipe_name: []}
        for ingredient in data[recipe_name]:
            converted[recipe_name].append(convert_ingredient(ingredient))

    if converted is None:
        return print("ERROR could not process recipe")

    return converted


def convert_ingredient(ingredient: dict):
    ingredient_name = (ingredient["ingredient"]).lower()
    if ingredient_name not in ingredient_densities:
        print(f"{ingredient_name} not able to convert")
        return {"ingredient": ingredient["ingredient"], "quantity": ingredient["quantity"],
                "measure": ingredient["measure"]}

    unit = ingredient["measure"]
    desired_unit = ingredient["desired"]
    quantity = float(ingredient["quantity"])
    density = ingredient_densities[ingredient_name]

    unit_is_mass = unit in (metric_mass_units + imperial_mass_units)
    unit_is_metric = unit in (metric_mass_units + metric_volume_units)
    desired_is_mass = desired_unit in (metric_mass_units + imperial_mass_units)
    desired_is_metric = desired_unit in (metric_mass_units + metric_volume_units)

    result = None

    # do we need to convert?
    if unit != desired_unit:
        # is conversion mass->mass
        if unit_is_mass and desired_is_mass:
            # metric mass conversion
            if unit_is_metric and desired_is_metric:
                result = quantity / metric_mass_unit_factors[unit]
                result = result * metric_mass_unit_factors[desired_unit]
            # imperial mass conversion
            elif unit_is_metric == desired_is_metric:
                result = quantity / imperial_mass_unit_factors[unit]
                result = result * imperial_mass_unit_factors[desired_unit]
            # metric->imperial conversion
            elif unit_is_metric:
                # convert to base unit (grams)
                result = quantity / metric_mass_unit_factors[unit]
                # metric to imperial
                result = result * metric_to_imperial_mass
                # to desired unit
                result = round(result * imperial_mass_unit_factors[desired_unit], 6)
            # imperial->metric conversion
            else:
                # convert to base unit (ounces)
                result = quantity / imperial_mass_unit_factors[unit]
                # convert imperial to metric
                result = result * imperial_to_metric_mass
                # convert to desired unit
                result = round(result * metric_mass_unit_factors[desired_unit], 6)
        # is conversion vol->vol
        elif unit_is_mass == desired_is_mass:
            # metric mass conversion
            if unit_is_metric and desired_is_metric:
                result = quantity / metric_volume_unit_factors[unit]
                result = result * metric_volume_unit_factors[desired_unit]
            # imperial mass conversion
            elif unit_is_metric == desired_is_metric:
                result = quantity / imperial_volume_unit_factors[unit]
                result = result * imperial_volume_unit_factors[desired_unit]
            # metric->imperial conversion
            elif unit_is_metric:
                # convert to base unit (l)
                result = quantity / metric_volume_unit_factors[unit]
                # metric to imperial
                result = result * metric_to_imperial_vol
                # to desired unit
                result = round(result * imperial_volume_unit_factors[desired_unit], 6)
            # imperial->metric conversion
            else:
                # convert to base unit (c)
                result = quantity / imperial_volume_unit_factors[unit]
                # convert imperial to metric
                result = result * imperial_to_metric_vol
                # convert to desired unit
                result = round(result * metric_volume_unit_factors[desired_unit], 6)
        # is conversion mass->vol
        elif unit_is_mass:
            # metric mass conversion
            if unit_is_metric and desired_is_metric:
                # convert to base unit (grams)
                result = quantity / metric_mass_unit_factors[unit]
                # convert mass to volume
                result = result * (1 / density)
                # imperial volume to metric volume
                result = result * imperial_to_metric_vol
                # convert to desired unit
                result = round(result * metric_volume_unit_factors[desired_unit], 6)
            # imperial mass conversion
            elif unit_is_metric == desired_is_metric:
                # convert to base unit (ounces)
                result = quantity / imperial_mass_unit_factors[unit]
                # convert to grams
                result = result * imperial_to_metric_mass
                # convert mass to volume
                result = result * (1 / density)
                # convert to desired unit
                result = round(result * imperial_volume_unit_factors[desired_unit], 6)
            # metric->imperial conversion
            elif unit_is_metric:
                # convert to base (grams)
                result = quantity / metric_mass_unit_factors[unit]
                # convert grams to cups
                result = result * (1 / density)
                # convert cups to desired unit
                result = round(result * imperial_volume_unit_factors[desired_unit], 6)
            # imperial->metric conversion
            else:
                # convert to base unit (ounces)
                result = quantity / imperial_mass_unit_factors[unit]
                # convert ounces to metric grams
                result = result * imperial_to_metric_mass
                # convert to cups via density
                result = result * (1 / density)
                # convert cups to metric liters
                result = result * imperial_to_metric_vol
                # convert to desired metric unit
                result = round(result * metric_volume_unit_factors[desired_unit], 6)
        # is conversion vol->mass
        else:
            # metric vol conversion
            if unit_is_metric and desired_is_metric:
                # convert to base unit (liters)
                result = quantity / metric_volume_unit_factors[unit]
                # convert to cups via metric to imperial vol
                result = result * metric_to_imperial_vol
                # convert to grams via density
                result = result * density
                # convert to desired via metric_mass_unit_factors
                result = round(result * metric_mass_unit_factors[desired_unit], 6)
            # imperial vol conversion
            elif unit_is_metric == desired_is_metric:
                # to base unit cups
                result = quantity / imperial_volume_unit_factors[unit]
                # to metric grams via density
                result = result * density
                # grams to ounces
                result = result * metric_to_imperial_mass
                # ounces to desired unit
                result = round(result * imperial_mass_unit_factors[desired_unit], 6)
            # metric->imperial conversion
            elif unit_is_metric:
                # convert to base (liters)
                result = quantity / metric_volume_unit_factors[unit]
                # convert to cups
                result = result * metric_to_imperial_vol
                # convert to grams via density
                result = result * density
                # convert to ounces
                result = result * metric_to_imperial_mass
                # convert to desired imperial mass
                result = round(result * imperial_mass_unit_factors[desired_unit], 6)
            # imperial->metric conversion
            else:
                # convert to base cups
                result = quantity / imperial_volume_unit_factors[unit]
                # convert to grams via density
                result = result * density
                # convert to desired mass
                result = round(result * metric_mass_unit_factors[desired_unit])

    return {"ingredient": ingredient["ingredient"], "quantity": str(result), "measure": desired_unit}


if __name__ == '__main__':
    data_1 = {
        "m->m": [
            # mass->mass metric
            {"ingredient": "all-purpose flour", "quantity": "100", "measure": "kg", "desired": "g"},
            # mass->mass imperial
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "lb", "desired": "oz"},
            # mass->mass imperial->metric
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "oz", "desired": "g"},
            # mass->mass metric->imperial
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "g", "desired": "oz"}
        ]
    }
    data_2 = {
        "v->v": [
            # vol->vol metric->imperial
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "ml", "desired": "c"},
            # vol->vol imperial->metric
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "c", "desired": "ml"},
            # vol->vol imperial
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "gal", "desired": "c"},
            # vol->vol mass
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "l", "desired": "ml"}
        ]
    }
    data_3 = {
        "m->v": [
            # mass->vol metric
            {"ingredient": "all-purpose flour", "quantity": "120", "measure": "g", "desired": "ml"},
            # mass->vol imperial
            {"ingredient": "all-purpose flour", "quantity": "16", "measure": "oz", "desired": "c"},
            # metric->imperial
            {"ingredient": "all-purpose flour", "quantity": "16", "measure": "g", "desired": "c"},
            # imperial->metric
            {"ingredient": "all-purpose flour", "quantity": "16", "measure": "oz", "desired": "l"}
        ]
    }
    data_4 = {
        "v->m": [
            # vol->mass metric
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "l", "desired": "g"},
            # vol->mass imperial
            {"ingredient": "all-purpose flour", "quantity": "1", "measure": "c", "desired": "oz"},
            # metric->imperial
            {"ingredient": "all-purpose flour", "quantity": "16", "measure": "l", "desired": "oz"},
            # imperial->metric
            {"ingredient": "all-purpose flour", "quantity": "16", "measure": "c", "desired": "g"}
        ]
    }

    print("MASS TO MASS")
    output = conversion(data_1)
    output_keys = list(output.keys())
    for key in output_keys:
        ingredients = output[key]
        for x in ingredients:
            print(x)

    print("VOL TO VOL")
    output = conversion(data_2)
    output_keys = list(output.keys())
    for key in output_keys:
        ingredients = output[key]
        for x in ingredients:
            print(x)

    print("MASS TO VOL")
    output = conversion(data_3)
    output_keys = list(output.keys())
    for key in output_keys:
        ingredients = output[key]
        for x in ingredients:
            print(x)

    print("VOL TO MASS")
    output = conversion(data_4)
    output_keys = list(output.keys())
    for key in output_keys:
        ingredients = output[key]
        for x in ingredients:
            print(x)