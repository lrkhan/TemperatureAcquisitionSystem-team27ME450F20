import numpy as np
import matplotlib.pyplot as plt


def get_data():

    batch_pre = np.array([[19.38, 18.90, 19.14, 19.54],
                          [19.86, 18.59, 17.35, 19.33],
                          [19.71, 19.12, 19.51, 19.63],
                          [19.06, 19.24, 19.79, 19.56],
                          [19.38, 19.47, 19.65, 19.47],
                          [19.53, 19.65, 19.31, 19.23],
                          [18.37, 19.84, 19.62, 19.20],
                          [19.58, 19.53, 19.49, 19.55],
                          [18.10, 18.83, 19.49, 19.32]])

    batch_1_sol = np.array([[19.13, 19.22, 19.31, 19.32],
                            [19.31, 19.29, 19.32, 19.35],
                            [19.43, 19.24, 19.30, 19.25],
                            [19.27, 19.46, 19.24, 19.36],
                            [19.31, 19.27, 19.42, 19.14],
                            [19.34, 19.32, 19.40, 19.40],
                            [19.27, 17.78, 19.71, 19.17],
                            [18.65, 19.31, 19.26, 19.55],
                            [19.50, 19.36, 19.34, 19.32]])

    batch_2_sol = np.array([[19.20, 19.34, 19.32, 19.42],
                            [19.34, 19.44, 19.30, 19.32],
                            [19.45, 19.43, 19.40, 19.42],
                            [19.22, 19.48, 19.09, 19.41],
                            [19.48, 19.29, 19.39, 19.07],
                            [19.23, 19.43, 19.08, 19.27],
                            [19.49, 19.42, 19.36, 19.22],
                            [19.22, 19.44, 19.28, 19.53],
                            [19.46, 19.47, 19.59, 19.49]])

    batch_3_sol = np.array([[19.33, 18.94, 18.80, 18.97],
                            [19.08, 19.24, 19.30, 19.45],
                            [19.45, 19.20, 19.39, 19.19],
                            [19.30, 19.50, 19.20, 19.40],
                            [19.39, 19.26, 19.28, 19.07],
                            [19.07, 19.25, 19.01, 19.11],
                            [19.50, 19.21, 19.53, 19.32],
                            [19.23, 19.30, 19.27, 19.46],
                            [19.27, 19.46, 19.46, 19.48]])

    batch_sol = np.stack((batch_1_sol, batch_2_sol, batch_3_sol), axis=0)

    return batch_sol,batch_pre


def warpage_prevention(batch_sol, batch_pre):
    """
    This function computes the metrics for validation of the warpage prevention specification
    """

    passing_percent = 1

    # median corner height of each batch. shape = (3,1,1) [solution batch]
    batch_median_sol = np.median(batch_sol, axis=(1, 2), keepdims=True)

    # deviation of each corner of each part from the batch median corner height [solution batch]
    batch_part_corner_deviation_sol = batch_sol - batch_median_sol

    # percent deviation of each corner of each part from the batch median corner height [solution batch]
    batch_part_corner_deviation_percent_sol = np.abs((batch_part_corner_deviation_sol / batch_median_sol)) * 100

    print(f"[solution batch]:{np.count_nonzero(batch_part_corner_deviation_percent_sol <= passing_percent)}/108 measurements is below {passing_percent}% pecent warpage")

    # median corner height. shape = (1,1) [initial batch]
    batch_median_pre = np.median(batch_pre, axis=1, keepdims=True)

    # deviation of each corner of each part from the median corner height [initial batch]
    batch_part_corner_deviation_pre = batch_pre - batch_median_pre

    # percent deviation of each corner of each part from its mean corner height [initial batch]
    batch_part_corner_deviation_percent_pre = np.abs(batch_part_corner_deviation_pre / batch_median_pre) * 100

    print(
        f"[initial batch]:{np.count_nonzero(batch_part_corner_deviation_percent_pre <= passing_percent)}/36 measurements is below {passing_percent}% pecent warpage")

    for i in range(1,5):
        batch_part_corner_deviation_percent_top_i_sol = np.sort(batch_part_corner_deviation_percent_sol, axis=2)[:, :,-i:]
        top_i_warpage_percent_sol = np.mean(batch_part_corner_deviation_percent_top_i_sol)
        batch_part_corner_deviation_percent_top_i_pre = np.sort(batch_part_corner_deviation_percent_pre, axis=1)[:,-i:]
        top_i_warpage_percent_pre = np.mean(batch_part_corner_deviation_percent_top_i_pre)
        print(top_i_warpage_percent_sol,top_i_warpage_percent_pre)
        warpage_percent_improvement_top_i = np.abs(top_i_warpage_percent_sol - top_i_warpage_percent_pre) / top_i_warpage_percent_pre

        print(f"Top {i} corner wapage improvement: {warpage_percent_improvement_top_i*100}%")
        # fig = plt.hist(np.sort(batch_part_corner_deviation_percent_pre, axis=1)[:,-i:].flatten())
        # plt.show()
        #fname = str(i)
        # plt.savefig(fname+'.png')
    return None


def consistency(batch_sol,batch_pre):

    passing_percent = 1

    batch_part_mean_sol = np.mean(batch_sol,axis=2,keepdims=True)
    # standard deviation of each part (relative to the part's mean corner height)
    batch_part_stdev_sol = np.std(batch_sol,axis = 2,keepdims= True)

    batch_part_stdev_percent_sol = (batch_part_stdev_sol / batch_part_mean_sol)*100

    print(f"[solution batch] {np.count_nonzero(batch_part_stdev_percent_sol<passing_percent)}/27 parts below {passing_percent}% part stdev relative to part mean")

    batch_part_mean_pre = np.mean(batch_pre, axis=1, keepdims=True)
    # standard deviation of each part (relative to the part's mean corner height)
    batch_part_stdev_pre = np.std(batch_pre, axis=1, keepdims=True)

    batch_part_stdev_percent_pre = (batch_part_stdev_pre / batch_part_mean_pre) * 100

    print(f"[initial batch] {np.count_nonzero(batch_part_stdev_percent_pre<passing_percent)}/9 parts below {passing_percent}% part stdev relative to part mean")


def first_pass_yield(batch_sol,batch_pre):

    print(f"[solution batch] {np.count_nonzero(np.min(batch_sol,axis=2) > 18.5)}/27 parts, {(np.count_nonzero(np.min(batch_sol,axis=2) > 18.5))/0.27}% FPY")
    print(f"[initial batch] {np.count_nonzero(np.min(batch_pre,axis=1) > 18.5)}/9 parts, {(np.count_nonzero(np.min(batch_pre,axis=1) > 18.5))/0.09}% FPY")


# print(batch_part_corner_deviation_percent_sol)

# # standard deviation of each part (relative to the part's mean corner height)
# batch_part_stdev_sol = np.std(batch_sol,axis = 2,keepdims= True)
#
# batch_part_stdev_percent_sol = batch_part_stdev_sol / batch_part_mean_sol





# batch_part_stdev_pre = np.std(batch_pre,axis = 1,keepdims=True)
#
# batch_part_stdev_percent_sol = batch_part_stdev_pre / batch_part_mean_pre
#
# print(np.max(np.abs(batch_part_corner_deviation_percent_pre)))

batch_sol,batch_pre = get_data()
global_mean_sol = np.mean(batch_sol)
global_stdev_sol = np.std(batch_sol)
global_mean_pre = np.mean(batch_pre)
global_stdev_pre = np.std(batch_pre)
batch_mean_sol = np.mean(batch_sol, axis=(1, 2), keepdims=True)
batch_stdev_sol = np.std(batch_sol, axis=(1, 2), keepdims=True)
mean_improve = (global_mean_sol - global_mean_pre) / global_mean_pre
stdev_improve = abs(global_stdev_sol - global_stdev_pre) / global_stdev_pre

print(f"Solution Mean:{global_mean_sol},Solution Stdev:,{global_stdev_sol}")
print(f"Previous Mean:{global_mean_pre},Previous Stdev:,{global_stdev_pre}")
print(f"Mean Improvement: {mean_improve*100} %, Stdev Improment: {stdev_improve*100}%")

# warpage_prevention(batch_sol,batch_pre)
first_pass_yield(batch_sol, batch_pre)
