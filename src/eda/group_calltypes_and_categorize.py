import pandas as pd
from os import path
from os import getcwd


def group_columns_by_call_type(dataframe, call_codes):
    '''
    dataframe is a pandas DataFrame object
    call_codes is a list of strings of codes that you want to group on, e.g. FEAB/FEAV or FEAL
    '''

    # Initialize the New Column Name
    new_column_name = "CODE_"

    # Make the column name
    for i in range(len(call_codes)):
        if i == 0:
            new_column_name = new_column_name + call_codes[i]
        else:
            new_column_name = new_column_name + "/" + call_codes[i]

    # Initialize the column with all the codes grouped
    dataframe[new_column_name] = 0

    # Get all columns that begin with the given code, these will be concatenated together
    list_of_columns = []
    for i in call_codes:
        list_of_columns = list_of_columns + [col for col in dataframe if col.startswith(i)]

    # Concatenate the columns in list of columns
    for i in list_of_columns:
        dataframe[new_column_name] = dataframe[new_column_name] + dataframe[i]

    # Drop the redundant concatenated columns
    for code in call_codes:
        reg = '^' + code
        dataframe = dataframe[dataframe.columns.drop(list(dataframe.filter(regex=reg)))]

    dataframe.columns = dataframe.columns.str.replace("CODE_", "")

    return dataframe


def get_wrangled_data(file):
    '''
    Take reads a csv that contains call types and demographic data
    Then adds the number of emergency categories for each block group
    :param file: CSV (either train_wrangled.csv or test_wrangled.csv)
    :return: CSV of call types which are grouped by 4 letter codes, the demographic data, and
             call type categories
    '''

    # Get into your Data Director
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    data_file = path.join(data_dir, file)

    # data file should look like '/Users/emreyurtbay/PycharmProjects/hfd-spring-2020/Data/train_wrangled.csv'
    data_frame = pd.read_csv(data_file)
    return data_frame


def main():
    # THE TRAIN PORTION

    # Train categories gets the count of each broad category of emergency
    train_categories = get_wrangled_data('train_categories.csv')

    # Pull train_wrangled
    train = get_wrangled_data("train_wrangled.csv")

    # Group by all the 4 letter codes in the dataframe
    train = group_columns_by_call_type(train, ["FEAB"])
    train = group_columns_by_call_type(train, ["FEAV"])
    train = group_columns_by_call_type(train, ["FEAL"])
    train = group_columns_by_call_type(train, ["FEAR"])
    train = group_columns_by_call_type(train, ["FEVR"])
    train = group_columns_by_call_type(train, ["FEAL"])
    train = group_columns_by_call_type(train, ["FEAS"])
    train = group_columns_by_call_type(train, ["FEBA"])
    train = group_columns_by_call_type(train, ["FEBI"])
    train = group_columns_by_call_type(train, ["FEBL"])
    train = group_columns_by_call_type(train, ["FEBU"])
    train = group_columns_by_call_type(train, ["FECA"])
    train = group_columns_by_call_type(train, ["FECH"])
    train = group_columns_by_call_type(train, ["FECP"])
    train = group_columns_by_call_type(train, ["FEDI"])
    train = group_columns_by_call_type(train, ["FEDR"])
    train = group_columns_by_call_type(train, ["FEEL"])
    train = group_columns_by_call_type(train, ["FEFA"])
    train = group_columns_by_call_type(train, ["FEFR"])
    train = group_columns_by_call_type(train, ["FEHD"])
    train = group_columns_by_call_type(train, ["FEHV"])
    train = group_columns_by_call_type(train, ["FEHG"])
    train = group_columns_by_call_type(train, ["FEHT"])
    train = group_columns_by_call_type(train, ["FEHU"])
    train = group_columns_by_call_type(train, ["FEHZ"])
    train = group_columns_by_call_type(train, ["FEIJ"])
    train = group_columns_by_call_type(train, ["FEIN"])
    train = group_columns_by_call_type(train, ["FEMA"])
    train = group_columns_by_call_type(train, ["FEMC"])
    train = group_columns_by_call_type(train, ["FEOB"])
    train = group_columns_by_call_type(train, ["FEOD"])
    train = group_columns_by_call_type(train, ["FEPD"])
    train = group_columns_by_call_type(train, ["FEPF"])
    train = group_columns_by_call_type(train, ["FEBV"])
    train = group_columns_by_call_type(train, ["FEOD"])
    train = group_columns_by_call_type(train, ["FEPO"])
    train = group_columns_by_call_type(train, ["FEPS"])
    train = group_columns_by_call_type(train, ["FERE"])
    train = group_columns_by_call_type(train, ["FESE"])
    train = group_columns_by_call_type(train, ["FESG"])
    train = group_columns_by_call_type(train, ["FESH"])
    train = group_columns_by_call_type(train, ["FESI"])
    train = group_columns_by_call_type(train, ["FEST"])
    train = group_columns_by_call_type(train, ["FESW"])
    train = group_columns_by_call_type(train, ["FESY"])
    train = group_columns_by_call_type(train, ["FETA"])
    train = group_columns_by_call_type(train, ["FETE"])
    train = group_columns_by_call_type(train, ["FEUC"])
    train = group_columns_by_call_type(train, ["FEUN"])
    train = group_columns_by_call_type(train, ["FEAM"])  # Possible Cardiac Arrest
    train = group_columns_by_call_type(train, ["FECK"])  # Check Patient
    train = group_columns_by_call_type(train, ["FEDA"])  # DEAD ON ARRIVAL
    train = group_columns_by_call_type(train, ["FEET"])  # Emergency Transfer
    train = group_columns_by_call_type(train, ["FESC"])  # Assist HPD
    train = group_columns_by_call_type(train, ["FEFD"])  # Self Initiated EMS Event?

    # Subset train_categories to only get the necessary columns
    categories = train_categories[['Block_Group', 'health',
                                   'injuries_external', "mental_illness", 'motor',
                                   'other', 'unknown']]

    # Merge the two data sets
    train_cat_and_calltype = train.merge(categories, left_on="Block_Group", right_on="Block_Group")

    # Save the data
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    train_cat_and_calltype_data_name = path.join(data_dir, 'train_with_categories_and_codes.csv')
    train_cat_and_calltype.to_csv(train_cat_and_calltype_data_name, index=False)

    # THE TEST PORTION

    # Read in the test data
    test = pd.read_csv('/Users/emreyurtbay/PycharmProjects/hfd-spring-2020/Data/test_wrangled.csv')

    # Merge Columns
    test = group_columns_by_call_type(test, ["FEAB"])
    test = group_columns_by_call_type(test, ["FEAV"])
    test = group_columns_by_call_type(test, ["FEAL"])
    test = group_columns_by_call_type(test, ["FEAR"])
    test = group_columns_by_call_type(test, ["FEVR"])
    test = group_columns_by_call_type(test, ["FEAL"])
    test = group_columns_by_call_type(test, ["FEAS"])
    test = group_columns_by_call_type(test, ["FEBA"])
    test = group_columns_by_call_type(test, ["FEBI"])
    test = group_columns_by_call_type(test, ["FEBL"])
    test = group_columns_by_call_type(test, ["FEBU"])
    test = group_columns_by_call_type(test, ["FECA"])
    test = group_columns_by_call_type(test, ["FECH"])
    test = group_columns_by_call_type(test, ["FECP"])
    test = group_columns_by_call_type(test, ["FEDI"])
    test = group_columns_by_call_type(test, ["FEDR"])
    test = group_columns_by_call_type(test, ["FEEL"])
    test = group_columns_by_call_type(test, ["FEFA"])
    test = group_columns_by_call_type(test, ["FEFR"])
    test = group_columns_by_call_type(test, ["FEHD"])
    test = group_columns_by_call_type(test, ["FEHV"])
    test = group_columns_by_call_type(test, ["FEHG"])
    test = group_columns_by_call_type(test, ["FEHT"])
    test = group_columns_by_call_type(test, ["FEHU"])
    test = group_columns_by_call_type(test, ["FEHZ"])
    test = group_columns_by_call_type(test, ["FEIJ"])
    test = group_columns_by_call_type(test, ["FEIN"])
    test = group_columns_by_call_type(test, ["FEMA"])
    test = group_columns_by_call_type(test, ["FEMC"])
    test = group_columns_by_call_type(test, ["FEOB"])
    test = group_columns_by_call_type(test, ["FEOD"])
    test = group_columns_by_call_type(test, ["FEPD"])
    test = group_columns_by_call_type(test, ["FEPF"])
    test = group_columns_by_call_type(test, ["FEBV"])
    test = group_columns_by_call_type(test, ["FEOD"])
    test = group_columns_by_call_type(test, ["FEPO"])
    test = group_columns_by_call_type(test, ["FEPS"])
    test = group_columns_by_call_type(test, ["FERE"])
    test = group_columns_by_call_type(test, ["FESE"])
    test = group_columns_by_call_type(test, ["FESG"])
    test = group_columns_by_call_type(test, ["FESH"])
    test = group_columns_by_call_type(test, ["FESI"])
    test = group_columns_by_call_type(test, ["FEST"])
    test = group_columns_by_call_type(test, ["FESW"])
    test = group_columns_by_call_type(test, ["FESY"])
    test = group_columns_by_call_type(test, ["FETA"])
    test = group_columns_by_call_type(test, ["FETE"])
    test = group_columns_by_call_type(test, ["FEUC"])
    test = group_columns_by_call_type(test, ["FEUN"])
    test = group_columns_by_call_type(test, ["FEAM"])  # Possible Cardiac Arrest
    test = group_columns_by_call_type(test, ["FECK"])  # Check Patient
    test = group_columns_by_call_type(test, ["FEDA"])  # DEAD ON ARRIVAL
    test = group_columns_by_call_type(test, ["FEET"])  # Emergency Transfer
    test = group_columns_by_call_type(test, ["FESC"])  # Assist HPD
    test = group_columns_by_call_type(test, ["FEFD"])  # Self Initiated EMS Event?

    # Read in the Categories
    test_categories = pd.read_csv('/Users/emreyurtbay/PycharmProjects/hfd-spring-2020/Data/test_categories.csv')

    # Subset the categories to get only the relevant columns
    categories = test_categories[['Block_Group', 'health',
                                  'injuries_external', "mental_illness", 'motor',
                                  'other']]

    # Merge
    test_cat_and_calltype = test.merge(categories, left_on="Block_Group", right_on="Block_Group")

    # Save to CSV file
    test_cat_and_calltype.to_csv(
        '/Users/emreyurtbay/PycharmProjects/hfd-spring-2020/Data/test_with_categories_and_codes.csv', index=False)


if __name__ == '__main__':
    main()
