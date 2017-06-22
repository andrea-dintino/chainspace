package uk.ac.ucl.cs.sec.chainspace;


/**
 *
 *
 */
public class Main {

    //
    private static final int CORES = 2;

    // verbose option prints out many comments on the console
    static final boolean VERBOSE = true;


    /*

     There are three debug options:
     (1) DEBUG: when DEBUG is enable, the core can run the same transaction multiple time; input objects are never set
     to inactive, and IDs don't need to be uniques in the databases.
     (2) DEBUG_CORE: the DEBUG_CORE option allows to test only the core: the checker is never called. Many nodes can be
     running but the application will behave as it was alone.
     (3) DEBUG_BFT: runs the node without calling BFTSmart; all objects are considered active.

        All debug options sould be set to false when running in production environement
     */
    static final boolean DEBUG_ALLOW_REPEAT         = true;
    static final boolean DEBUG_SKIP_CHECKER         = false;
    static final boolean DEBUG_NO_BROADCAST         = true;
    static final boolean DEBUG_IGNORE_DEPENDENCIES  = false;
    //static final boolean DEBUG_SKIP_BFT    = false;


    /**
     * main
     * @param args not used
     */
    public static void main(String[] args) {

        // verbose print
        if (Main.VERBOSE) { Utils.printHeader("Starting Chainsapce..."); }


        // run chainspace service
        for (int i = 1; i <= CORES; i++) {
            runNodeService(i);
        }


        // verbose print
        if (Main.VERBOSE) { Utils.printLine(); }

    }


    /**
     * runNodeService
     * Run a node service with a given node's ID.
     * @param nodeID the node's ID
     */
    private static void runNodeService(int nodeID) {

        try {

            // run a new node instance
            new NodeService(nodeID);

        }
        catch (Exception e) {
            if (Main.VERBOSE) { Utils.printStacktrace(e); }
            else { System.err.println("[ERROR] Node service #" +nodeID+ " failled to start."); }
        }

    }

}
