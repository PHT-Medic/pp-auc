from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from main import *
import json
from collections import Counter
from FHM_approx import *

d = {
    'A': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'R': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'N': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'D': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'C': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'E': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Q': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'G': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'H': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'I': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'L': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'M': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'F': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'P': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'S': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'T': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'W': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'Y': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'V': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    '-': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'X': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}


class Train:
    def __init__(self, model=None, results=None):
        """
        :param results:
        """
        self.results = results
        self.encoded_model = model

    def load_results(self):
        """
        If a result file exists, loads the results, otherwise will return empty results.
        :return:
        """
        try:
            with open(self.results, 'rb') as results_file:
                return pickle.load(file=results_file)
        except Exception:
            return {'initial': False,
                    'proxy': False,
                    'station': -1,
                    'data_approx': [],
                    'data_exact': [],
                    'per': {'DPPA-AUC': {'samples': [],
                                       'flags': [],
                                       'total_time': []},
                            'DPPE-AUC': {'samples': [],
                                      'flags': [],
                                      'total_time': []}
                            },
                    'times': {'approx': {"init": [],
                                         "station_1": [],
                                         "proxy": [],
                                         "station_2": [],
                                         "s_1_total": []},
                              'exact': {"init": [],
                                        "station_1": [],
                                        "proxy": [],
                                        "station_2": [],
                                        "s_1_total": []}},
                    'approx': {'enc_rx': {},
                               'enc_s_p_sks': [],
                               'users_rsa_pk': [],
                               'pp_auc_tables': {},
                               'encrypted_ks': [],
                               'encrypted_r1': {},  # index is used by station i
                               'encrypted_r2': {},
                               'aggregator_rsa_pk': {},
                               'aggregator_paillier_pk': {},
                               'stations_paillier_pk': {},
                               'stations_rsa_pk': {},
                               'proxy_encrypted_r_N': {},  # index 0 = r1_iN; 1 = r2_iN
                               'D1': [],
                               'D2': [],
                               'D3': [],
                               'N1': [],
                               'N2': [],
                               'N3': []
                               },
                    'exact': {'enc_rx': {},
                              'enc_s_p_sks': [],
                              'users_rsa_pk': [],
                              'enc_agg_sk_1': {},
                              'enc_agg_sk_2': {},
                              'pp_auc_tables': {},
                              'encrypted_ks': [],
                              'encrypted_r1': {},  # index is used by station i
                              'encrypted_r2': {},
                              'aggregator_rsa_pk': {},
                              'aggregator_paillier_pk': {},
                              'stations_paillier_pk': {},
                              'stations_rsa_pk': {},
                              'proxy_encrypted_r_N': {},  # index 0 = r1_iN; 1 = r2_iN
                              'D1': [],
                              'D2': [],
                              'D3': [],
                              'N1': [],
                              'N2': [],
                              'N3': []
                              }
                    }

    def save_results(self, results):
        """
        Saves the result file of the train
        :param results:
        :return:
        """
        try:
            with open(self.results, 'wb') as results_file:
                return pickle.dump(results, results_file)
        except Exception as err:
            print(err)
            raise FileNotFoundError("Result file cannot be saved")

    def save_model(self, model):
        with open(self.encoded_model, "wb") as model_file:
            pickle.dump(model, model_file)

    def load_model(self):
        try:
            with open(self.encoded_model, "rb") as model_file:
                model = pickle.load(model_file)
            print("Loading previous model")
            return model
        except Exception:
            print("No previous model")
            return None


def data_generation(pre, label, data_path, station, save, approx):
    real_data = {"Pre": pre, "Label": label, "Flag": [1] * len(label)}
    df_real = pd.DataFrame(real_data)
    df_real.sort_values('Pre', ascending=False, inplace=True)

    if approx:
        if save:
            df_real.to_pickle(f"{data_path}/data_s{station + 1}.pkl")
        return df_real
    # Create synthetic data
    unique_vals = df_real['Pre'].unique()
    counts = df_real['Pre'].value_counts()
    highest_count = counts.max()

    # Adjust the distribution to generate synthetic data
    synthetic_pre = []
    for val in unique_vals:
        repetitions = highest_count - counts[val]
        if repetitions > 0:
            synthetic_pre.extend([val] * repetitions)

    synthetic_data = {
            "Pre": synthetic_pre,
            "Label": [0] * len(synthetic_pre),  # Assign synthetic data a fixed label of 0
            "Flag": [0] * len(synthetic_pre)  # Indicate synthetic data with Flag = 0
    }
    df_fake = pd.DataFrame(synthetic_data)

    # Merge real and synthetic data
    df = pd.concat([df_real, df_fake], ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the combined dataset

    # Ensure consistency: set Label = 0 where Flag = 0
    df.loc[df["Flag"] == 0, "Label"] = 0

    if save:
        df.to_pickle(f"{data_path}/data_s{station + 1}.pkl")
    unique_vals = df_real['Pre'].unique()
    min_subjects = 3  # Fixed minimal number of synthetic subjects per unique value

    synthetic_pre = []
    for val in unique_vals:
        synthetic_pre.extend([val] * min_subjects)

    # Create synthetic data
    synthetic_data = {
        "Pre": synthetic_pre,
        "Label": [0] * len(synthetic_pre),  # Label = 0 for synthetic data
        "Flag": [0] * len(synthetic_pre)  # Flag = 0 for synthetic data
    }
    df_fake = pd.DataFrame(synthetic_data)

    # Combine real and synthetic data
    df = pd.concat([df_real, df_fake], ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the dataset

    # Ensure consistency: Label = 0 where Flag = 0
    df.loc[df["Flag"] == 0, "Label"] = 0

    # Optional: Save the dataset
    if save:
        df.to_pickle(f"{data_path}/data_s{station + 1}.pkl")
    plot_input_data(df, df_real, df_fake, station-1, proxy=False)
    return df


def initial_station(results, conf_path):
    # print(os.getenv("PRIVATE_KEY_PATH"))
    # Get users, and all stations PK
    with open(conf_path, 'r') as f:
        trainConfig = json.load(f)

    rsa_pks = []
    for i in range(len(trainConfig['route'])):
        rsa_pks.append(bytes.fromhex(trainConfig['route'][i]['rsa_public_key']))

    print('prepared keys for {} stations'.format(len(rsa_pks)))
    results['stations_rsa_pk'] = rsa_pks  # 0 init 1 station 2 station n+1 proxy
    results['aggregator_rsa_pk'] = rsa_pks[-1]

    user_pk = bytes.fromhex(trainConfig['creator']['rsa_public_key'])
    results['users_rsa_pk'] = user_pk

    # Stations Paillier Keys
    env_symm_key = Fernet.generate_key()
    for i in range(len(rsa_pks)):
        sk, pk = generate_keypair(3072)  # paillier keys for stations

        enc_sk = {'n': Fernet(env_symm_key).encrypt(bytes(str(sk.n), 'utf-8')),
                  'x': Fernet(env_symm_key).encrypt(bytes(str(sk.x), 'utf-8'))
                  }
        results['enc_s_p_sks'].append(enc_sk)
        results['stations_paillier_pk'][i] = pk

    # Aggregator Paillier Keys
    sk, pk = generate_keypair(3072)
    sk_1 = copy.copy(sk)
    sk_2 = copy.copy(sk)

    enc_sk_1 = {'n': Fernet(env_symm_key).encrypt(bytes(str(sk_1.n), 'utf-8')),
                'nsqr': Fernet(env_symm_key).encrypt(bytes(str(sk_1.nsqr), 'utf-8')),
                'x1': Fernet(env_symm_key).encrypt(bytes(str(sk_1.x1), 'utf-8'))
                }
    results['enc_agg_sk_1'] = enc_sk_1

    enc_sk_2 = {'n': Fernet(env_symm_key).encrypt(bytes(str(sk_2.n), 'utf-8')),
                'nsqr': Fernet(env_symm_key).encrypt(bytes(str(sk_2.nsqr), 'utf-8')),
                'x2': Fernet(env_symm_key).encrypt(bytes(str(sk_1.x2), 'utf-8'))
                }

    enc_env_key = []
    for i in range(len(rsa_pks)):
        enc_env_key.append(rsa_encrypt(env_symm_key, rsa_pks[i]))
    enc_env_key.append(rsa_encrypt(env_symm_key, user_pk))
    results['enc_symm_key'] = enc_env_key
    results['enc_agg_sk_2'] = enc_sk_2  # for all stations and users partial Pailler private key

    results['aggregator_paillier_pk'] = pk

    # simulate private key separation for the aggregator
    del sk_1.x2
    del sk_1.x

    del sk_2.x1
    del sk_2.x
    return results


def execution_simulation(conf_path, sk_path):
    DIRECTORY = os.getcwd()

    print("Comparing DPPE-AUC and DPPA-AUC in same run")
    MAX = 100000
    no_of_decision_points = 100

    decision_points = np.linspace(0, 1, num=no_of_decision_points)[::-1]

    MODEL_PATH = DIRECTORY + '/model.pkl'
    RESULT_PATH = DIRECTORY + '/results.pkl'
    train = Train(model=MODEL_PATH, results=RESULT_PATH)

    # Init station: create keys, save init
    results = train.load_results()

    times = results['times']
    data_exact = results['data_exact']
    data_approx = results['data_approx']

    stations = results['station'] + 1
    print('Station: {}'.format(stations))

    results['station'] = stations  # save new value

    if not results['initial']:
        print('Station Init - Create and encrypt keys')
        t0 = time.perf_counter()
        results['approx'] = initial_station(results['approx'], conf_path)
        t1 = time.perf_counter()
        times['approx']["init"].append(t1 - t0)
        print(f'Key creation approximation method time {sum(times["approx"]["init"]):0.4f} seconds')

        t0 = time.perf_counter()
        results['exact'] = initial_station(results['exact'], conf_path)
        t1 = time.perf_counter()
        times['exact']["init"].append(t1 - t0)
        print(f'Key creation approximation method time {sum(times["exact"]["init"]):0.4f} seconds')
        results['initial'] = True
        results['times'] = times
        train.save_results(results)
        print('Keys saved')
        # exit(0)
    elif not results['proxy']:
        # Station part I: load data, train model, save model, save data
        filename = DIRECTORY + '/sequences_s' + str(stations) + '.txt'
        data = defaultdict(list)
        model = train.load_model()

        feature_len = None
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                spt = line.split()
                seq = spt[1].strip()
                label = spt[2].strip()
                item = []
                for ch in seq:
                    item.extend(d[ch])
                N = len(item)
                if feature_len is None:
                    feature_len = N
                else:
                    if feature_len != N:
                        raise ValueError
                data[label].append(item)
        print("Number of data points for model training:", {key: len(value) for (key, value) in data.items()})
        data = {'CXCR4': data['CXCR4'],
                'CCR5': data['CCR5']}

        X = []
        Y = []
        total_s1_approx, total_s1_exact = 0, 0

        for j in range(len(data['CCR5'])):
            X.append(data['CCR5'][j])
            Y.append(1)
            try:
                X.append(data['CXCR4'][j])
                Y.append(0)
            except Exception:
                pass

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.10, random_state=1, shuffle=True)
        print('Hold out test size for comparison of methods: {}'.format(Counter(y_test)))

        if model is None:
            model = GradientBoostingClassifier()

        model.fit(x_train, y_train)

        # START DPPE Protocol
        y_pred_prob = model.predict_proba(x_test)[:, -1]
        pre = np.array(y_pred_prob)

        label = y_test
        exact_stat_df = data_generation(pre, label, DIRECTORY + '/pht_results/', stations, save=False, approx=False)
        approx_stat_df = data_generation(pre, label, DIRECTORY + '/pht_results/', stations, save=False, approx=True)

        data_approx.append(approx_stat_df.copy())
        data_exact.append(exact_stat_df.copy())

        print('Station - DPPA-AUC protocol - Step I')
        t1 = time.perf_counter()
        results['approx'] = dppa_auc_protocol(approx_stat_df, decision_points, results["approx"],
                                           station=int(stations), max_value=MAX, rsa_sk_path=sk_path)
        t2 = time.perf_counter()
        times['approx']["station_1"].append(t2 - t1)
        print(f'Approx execution time by station {times["approx"]["station_1"][-1]:0.4f} seconds')

        print('Station - DPPE-AUC protocol - Step I')
        t1 = time.perf_counter()
        results['exact'] = dppe_auc_protocol(exact_stat_df, results["exact"], station=int(stations),
                                             max_value=MAX, rsa_sk_path=sk_path)
        t2 = time.perf_counter()
        times['exact']["station_1"].append(t2 - t1)
        print(f'Exact execution time by station {times["exact"]["station_1"][-1]:0.4f} seconds')

        total_s1_approx += times['approx']["station_1"][-1]
        total_s1_exact += times['exact']["station_1"][-1]

        times['approx']['s_1_total'].append(total_s1_approx)
        times['exact']['s_1_total'].append(total_s1_exact)

        results['data_approx'] = data_approx
        results['data_exact'] = data_exact

        train.save_model(model)

        if stations == len(results['approx']['stations_rsa_pk']) - 2:  # in dev -1
            results['proxy'] = True

        train.save_results(results)
    elif results['proxy']:
        #  Proxy Computation
        print('Starting proxy protocol')

        # times['approx']['s_1_total'].append(total_s1_approx)
        # times['exact']['s_1_total'].append(total_s1_exact)
        t3 = time.perf_counter()
        results['approx'] = dppa_auc_proxy(results["approx"], max_value=MAX, no_dps=no_of_decision_points, sk_path=sk_path)
        t4 = time.perf_counter()
        times["approx"]['proxy'].append(t4 - t3)
        print(f'Approx execution time by proxy station {times["approx"]["proxy"][-1]:0.4f} seconds')

        t3 = time.perf_counter()
        results['exact'] = dppe_auc_proxy(results["exact"], max_value=MAX, sk_path=sk_path)
        t4 = time.perf_counter()
        times["exact"]['proxy'].append(t4 - t3)
        print(f'Exact execution time by proxy station {times["exact"]["proxy"][-1]:0.4f} seconds')

        results['times'] = times
        train.save_results(results)

    # Final: User has locally to run last step


def user_part(res_path, sk_path, sk_pw):
    DIRECTORY = os.getcwd()
    print("Comparing both approaches in same run")

    approx_auc_diff, exact_auc_diff = [], []
    approx_total_times, exact_total_times = [], []
    MODEL_PATH = DIRECTORY + '/pht_results/model.pkl'

    train = Train(model=MODEL_PATH, results=res_path)
    results = train.load_results()

    times = results['times']
    per = results['per']
    data_approx = results['data_approx']
    data_exact = results['data_exact']
    stations = len(times["approx"]['station_1'])
    print('Station - DPPE-AUC & FHAUC-AUC protocol - Step II')

    auc_gt_approx, per['DPPA-AUC'] = calculate_regular_auc(1, per['DPPA-AUC'], data=data_approx, APPROX=True)
    print('Approx GT-AUC: ', auc_gt_approx)
    auc_gt_exact, per['DPPE-AUC'] = calculate_regular_auc(1, per['DPPE-AUC'], data=data_exact, APPROX=False)
    print('Exact GT-AUC: ', auc_gt_exact)

    t1 = time.perf_counter()
    auc_pp_exact = pp_auc_station_final(results["exact"], sk_path, sk_pw, APPROX=True)
    t2 = time.perf_counter()
    times['exact']['station_2'].append(t2 - t1)
    print('\n')
    total_time_exact = times["exact"]['s_1_total'][-1] + times["exact"]['proxy'][-1] + (
            times["exact"]['station_2'][-1] * len(times["approx"]['station_1']))
    print(f'Exact execution time by User - Step II {times["exact"]["station_2"][-1]:0.4f} seconds')



    t5 = time.perf_counter()
    auc_pp_approx = pp_auc_station_final(results["approx"], sk_path, sk_pw, APPROX=True)
    t6 = time.perf_counter()

    times['approx']['station_2'].append(t6 - t5)

    # Compute total approximate time for the current run
    total_time_approx = (
            times["approx"]['s_1_total'][-1] +
            times["approx"]['proxy'][-1] +
            (times["approx"]['station_2'][-1] * stations)
    )

    # Display the execution time for station 2 and total approximate time
    print(f'Approx execution time by station - Step II {times["approx"]["station_2"][-1]:0.4f} seconds')
    print(f'Approx total time {total_time_approx}')
    print(f'Exact total time {total_time_exact}')

    # Append the exact total time for this run
    per['DPPE-AUC']['total_time'].append(total_time_exact)
    exact_total_times.append(total_time_exact)

    # Calculate and store the AUC differences for exact data
    diff_exact = auc_gt_exact - auc_pp_exact
    exact_auc_diff.append(diff_exact)

    # Compute and display average exact AUC difference
    exact_avg_diff = sum(exact_auc_diff) / len(exact_auc_diff)
    print(
        f'Exact average differences over {len(exact_auc_diff)} runs: Average = {exact_avg_diff}, All differences = {exact_auc_diff}')

    # Calculate and store the AUC differences for approximate data
    diff_approx = auc_gt_approx - auc_pp_approx
    approx_auc_diff.append(diff_approx)

    # Compute and display average approximate AUC difference
    approx_avg_diff = sum(approx_auc_diff) / len(approx_auc_diff)
    print(
        f'Approx average differences over {len(approx_auc_diff)} runs: Average = {approx_avg_diff}, All differences = {approx_auc_diff}')


def run_demo_simulation(conf_path, station_rsa_sk_path, sk_path, sk_pw, res_path):
    for i in range(5):
        execution_simulation(conf_path, station_rsa_sk_path)
        print('\n')

    user_part(res_path, sk_path, sk_pw)

if __name__ == '__main__':
    res_path = './results.pkl'
    sk_path = './conf/demo.pem'
    sk_pw = 'start123'
    station_rsa_sk_path = './conf/key.pem'
    conf_path = './conf/train_config.json'

    files_to_delete = ['results.pkl', 'model.pkl']

    # Delete each file if it exists
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)

    run_demo_simulation(conf_path, station_rsa_sk_path, sk_path, sk_pw, res_path)
