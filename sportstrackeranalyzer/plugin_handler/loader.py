from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector, NameCollector, ClassCollector
from sportstrackeranalyzer.plugins.plugin_simple_distances import Plugin_SimpleDistance


class PluginLoader():

    def __init__(self):
        """
        Init the PluginLoader for the good. We can load and process

        """
        self.dbh = None
        self.track_hash = None
        self.existing_leaves = None
        self.existing_leave_names = None
        self.overwrite = False

    def allow_overwrite(self):
        """
        If activated, you are allowed to reprocess and re-write the plugins which are
        existing already.
        :return:
        """
        self.overwrite = True

    def get_all_plugins(self):
        """
        Extract all available plugins/leaves in the "plugins" folder.
        :return:
        """
        return NameCollector

    def set_database_handler(self, dbh):
        """
        Handover a database handler such it is defined within in db_handler.py
        We are going to use the db_handler.py here. In case we want to change
        to some other handler, mind that you need to adjust the member functions.

        :param dbh: A database handler from db_handler.py
        :return: -
        """
        self.dbh = dbh

    def set_track_by_hash(self, track_hash):
        """
        The PluginLoader can process many plugins. Therefore, this member
        function setup your track information to which the database
        handler will interact with
        :param track_hash: A hash (string)
        :return:
        """
        self.track_hash = track_hash

    def set_existing_leaves_for_track(self, existing_leaves):
        """
        Prepare the PluginLoader with existing leaves.
        :param existing_leaves:
        :return:
        """
        self.existing_leaves = existing_leaves
        self.existing_leave_names = list(existing_leaves.keys())

    def process(self, plugin_name):
        """
        The processor - This
        :param plugin_name:
        :return:
        """

        # Step 1: Init the plugin
        process_obj = ClassCollector[plugin_name]
        process_obj.init()

        # Request objects: Get the plugin configuration
        leaf_config = process_obj.get_plugin_config()

        # For simplicity, we extract leaf name and dependencies here:
        leaf_name = leaf_config.get("leaf_name")
        required_leaves = leaf_config.get("module_dependencies")

        # check if according leaf exists already:
        if leaf_name in self.existing_leave_names and self.overwrite is False:
            # return 2: Plugin/Leaf is satisfied already
            return 2

        # if not, check if necessary perquisites exits as leaves:
        check_if_in_list = any(item in required_leaves for item in self.existing_leave_names)
        if check_if_in_list is False:
            # return 1: There was a problem with pre-existing leaves. In that case, we
            # need to think a bit how to proceed here...
            return 1

        # This plugin needs certain prequisits to be loaded in memory (pandas DataFrame)
        # We do this here and safe the DataFrames in a dictionary for the later processing
        leaves_db = {} # Holds all DataFrames
        for i_leaf in required_leaves:
            # We know that leaves exist already, so let's do just like this:
            i_leaf_name = self.existing_leaves.get(i_leaf).get("name")
            i_leaf_hash = self.existing_leaves.get(i_leaf).get("leaf_hash")

            df_i = self.dbh.read_leaf(directory=i_leaf_name,
                                      leaf_hash=i_leaf_hash,
                                      leaf_type="DataFrame")
            leaves_db[i_leaf] = df_i

        # After we have gathered our DataFrames for processing, let's hand them over
        process_obj.set_plugin_data(leaves_db)

        # Run the processor:
        process_obj.run()

        # Extract the processed data:
        proc_success = process_obj.get_processing_success() # Was processing successful?
        df_result = process_obj.get_result() # A DataFrame with the result

        print(proc_success)
        print(df_result)

        if proc_success is True:
            # If we have a positive message on processing, we go on

            # Extract the columns of the DataFrame for the leaf configuration:
            obj_definition = list(df_result.columns)

            # Create leaf configuration:
            leaf_config_final = self.dbh.create_leaf_config(leaf_name=leaf_name,
                                                      track_hash=self.track_hash,
                                                      columns=obj_definition)

            # Write the leave configuration to our track/branch database:
            r = self.dbh.write_leaf(track_hash=self.track_hash,
                               leaf_config=leaf_config_final,
                               leaf=df_result,
                               leaf_type="DataFrame"
                               )
            # if everything is fine, we return 0
            return 0
        else:
            print(f"The plugin {plugin_name} (leaf name {leaf_name}) could not be processed")
            print(f"Abort here")
            return -1
