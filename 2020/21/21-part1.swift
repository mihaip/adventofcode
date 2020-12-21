#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let regex = try! NSRegularExpression(pattern: #"(.+) \(contains (.+)\)"#, options: [])

    let lines = inputStr.components(separatedBy: .newlines)

    var allergensToIngredients = Dictionary<String, Set<String>>()
    var ingredientCounts = Dictionary<String, Int>()

    for line in lines {
        if let match = regex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let ingredientsStr = line[Range(match.range(at: 1), in: line)!]
            let allergensStr = line[Range(match.range(at: 2), in: line)!]
            let ingredients = ingredientsStr.components(separatedBy: " ")
            let allergens = allergensStr.components(separatedBy: ", ")

            for ingredient in ingredients {
                if let count = ingredientCounts[ingredient] {
                    ingredientCounts[ingredient] = count + 1
                } else {
                    ingredientCounts[ingredient] = 1
                }
            }
            for allergen in allergens {
                if let existingIngredients = allergensToIngredients[allergen] {
                    allergensToIngredients[allergen] = existingIngredients.intersection(ingredients)
                } else {
                    allergensToIngredients[allergen] = Set(ingredients)
                }
            }
        }
    }

    var ingredientsToAllergens = Dictionary<String, Set<String>>()
    for (allergen, ingredients) in allergensToIngredients {
        for ingredient in ingredients {
            if ingredientsToAllergens[ingredient] != nil {
                ingredientsToAllergens[ingredient]!.insert(allergen)
            } else {
                ingredientsToAllergens[ingredient] = Set([allergen])
            }
        }
    }

    var sum = 0
    for (ingredient, count) in ingredientCounts {
        if ingredientsToAllergens[ingredient] == nil {
            sum += count
        }
    }
    print("answer", sum)

}

main()
