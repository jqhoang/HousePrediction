#flat vs percentage graph
#only consider cv err
#x axis boundary 400 - 1600
#y axis error
#3 lines each for each model
import matplotlib.pyplot as plt
#rf, linear, lasso

test_flat_err = [
    (72440.49122205564, 121226.96309766304, 123874.12955362927),
    (69117.36901052459, 124823.8619781703, 127950.86446820597),
    (72417.678134139, 129457.15873814118, 131180.42638980024),
    (72453.89832730118, 128740.83076960656,131116.00490852687)
    ]
test_prop_err = [
    (0.04848967504275213, 0.09732304278034012,  0.09815561587848842),
    (0.045183632946910204, 0.09446487430575998, 0.0952325573309474),
    (0.04647075702684119, 0.09567169825217899, 0.09658209178754747),
    (0.04586959418269423, 0.09615141539077578, 0.09755576203440855)
    ]

test_flat_r2 = [
    (0.7458627391049937,0.5931075706480247,0.5817300786629227),
    (0.7948435823145588, 0.6173222704465373,0.6062384716585438),
    (0.7836630709993495, 0.6094359120284429,0.5975405743819302),
    (0.7847344601327709, 0.6129790190002131,0.6004199241794403)
    ]
test_prop_r2 = [
    (0.7204346954949143, 0.36434319774443524,0.36052522883107685),
    (0.7418706483450737, 0.3796168547452128,0.37485390580953193),
    (0.7484897320872803, 0.3800676734391434,0.37489870421529525),
    (0.7503979494795742, 0.3793791196854802,0.3689736684766748)
    ]
boundaries = [400,800,1200,1600]

plt.figure("Predicting Flat Property Value Change With Both Data Types")
random_forest, linear_regression, lasso = plt.plot(boundaries, test_flat_err)
random_forest.set_label("Random Forest")
linear_regression.set_label("Linear Regression")
lasso.set_label("Lasso Regression")
plt.title("Predicting Flat Property Value Change With Both Data Types")
plt.xlabel("Boundary Size (m)")
plt.ylabel("Test Error")
plt.legend()

plt.figure("Predicting Porportional Property Value Change With Both Data Types")
random_forest, linear_regression, lasso = plt.plot(boundaries, test_prop_err)
random_forest.set_label("Random Forest")
linear_regression.set_label("Linear Regression")
lasso.set_label("Lasso Regression")
plt.title("Predicting Porportional Property Value Change With Both Data Types")
plt.xlabel("Boundary Size (m)")
plt.ylabel("Test Error")
plt.legend()

plt.figure("R^2 Value of Flat Predictions")
random_forest, linear_regression, lasso = plt.plot(boundaries, test_flat_r2)
random_forest.set_label("Random Forest")
linear_regression.set_label("Linear Regression")
lasso.set_label("Lasso Regression")
plt.title("R^2 Value of Flat Predictions")
plt.xlabel("Boundary Size (m)")
plt.ylabel("R^2")
plt.legend()

plt.figure("R^2 Value of Proportional Predictions")
random_forest, linear_regression, lasso = plt.plot(boundaries, test_prop_r2)
random_forest.set_label("Random Forest")
linear_regression.set_label("Linear Regression")
lasso.set_label("Lasso Regression")
plt.title("R^2 Value of Proportional Predictions")
plt.xlabel("Boundary Size (m)")
plt.ylabel("R^2")
plt.legend()


plt.show()
