 $(function() {

          var ingNum = parseInt($("#newIngCount").val()); 
          var stepNum = parseInt($("#newStepCount").val()); 
          var max = 15; 
          var ingredientWrap = $(".ingredient"); 
          var addIngredient = $(".newIngredient"); 
          var stepWrap = $(".step"); 
          var addStep = $(".newStep");

          $(addIngredient).click(function(e){ 
              e.preventDefault();
              if(ingNum < max){ 
                ingNum++;
                $(ingredientWrap).append('<div class="form-group col-md-8"><input type="text" class="form-control inputIngredient" name="ing' + ingNum + 'Title" placeholder="Ingredient"></div><div class="form-group col-md-2"><input type="number" class="form-control inputAmount" name="ing' + ingNum + 'Amt" placeholder="Amount"></div><div class="form-group col-md-2"><select class="form-control" name="ing' + ingNum + 'Unit"><option selected>Unit</option><option value="grams">grams</option><option value="cups">cups</option><option value="ounces">ounces</option><option value="pounds">pounds</option><option value="milliliters">milliliters</option><option value="tablespoon">tablespoon</option><option value="teaspoon">teaspoon</option><option value=" ">whole ingredient</option></div>');
              }
          });
          
          $(addStep).click(function(e){ 
              e.preventDefault();
              if(stepNum < max){ 
                stepNum++; 
                $(stepWrap).append('<div class="form-group"><input type="text" class="form-control inputStep" name="step' + stepNum + '" placeholder="Enter the next step necessary for the recipe!"></div>');
              }
          });
      });