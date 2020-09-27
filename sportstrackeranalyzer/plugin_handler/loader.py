from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector, NameCollector, ClassCollector
from sportstrackeranalyzer.plugins.plugin_simple_distances import Plugin_SimpleDistance


class PluginLoader():

    def __init__(self):
        self.dbh = None
        self.track_hash = None
        self.existing_leaves = None
        self.existing_leave_names = None

        print("Init PluginLoader")


    def get_all_plugins(self):
        return NameCollector

    def set_database_handler(self, dbh):
        self.dbh = dbh

    def set_track_by_hash(self, track_hash):
        self.track_hash = track_hash

    def set_existing_leaves_for_track(self, existing_leaves):
        self.existing_leaves = existing_leaves
        self.existing_leave_names = list(existing_leaves.keys())

    def process(self, plugin_name):
        print(plugin_name)
        # Step 1: Init()
        process_obj = ClassCollector[plugin_name]
        process_obj.init()

        # Request objects
        leaf_config = process_obj.get_plugin_config()

        leaf_name = leaf_config.get("leaf_name")
        required_leaves = leaf_config.get("module_dependencies")

        # leaves = self.dbh.get_all_leaves_for_track(track_hash=i_track_hash)
        print("required plugins:", required_leaves)
        print("leaf names:", leaf_name)
        print("existing leaves:", self.existing_leave_names)
        # check if according leaf exists already:

        if leaf_name in self.existing_leave_names:
            # return 2: Plugin/Leaf is satisfied already
            return 2

        # if not, check if necessary perquisites exits as leaves:
        check_if_in_list = any(item in required_leaves for item in self.existing_leave_names)
        if check_if_in_list is False:
            # return 1: There was a problem with pre-existing leaves
            return 1


        # Extract leaves from database:
        leaves_db = {}
        for i_leaf in required_leaves:

            i_leaf_name = self.existing_leaves.get(i_leaf).get("name")
            i_leaf_hash = self.existing_leaves.get(i_leaf).get("leaf_hash")
            print(i_leaf_name, i_leaf_hash)

            df_i = self.dbh.read_leaf(directory=i_leaf_name,
                                      leaf_hash=i_leaf_hash,
                                      leaf_type="DataFrame")
            leaves_db[i_leaf] = df_i

        process_obj.set_plugin_data(leaves_db)

        # Run the processor:
        process_obj.run()

        # Extract the processed data:
        proc_success = process_obj.get_processing_success()
        df_result = process_obj.get_result()

        print(proc_success)
        print(df_result)

        obj_definition = list(df_result.columns)
        # Create leaf configuration:
        leaf_config_final = self.dbh.create_leaf_config(leaf_name=leaf_name,
                                                  track_hash=self.track_hash,
                                                  columns=obj_definition)
        print(leaf_config_final)
        # Write the second leaf:
        # r = dbh.write_leaf(track_hash=hash_str,
        #                    leaf_config=leaf_config,
        #                    leaf=df_metadata,
        #                    leaf_type="DataFrame"
        #                    )